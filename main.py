import json
from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
import langfeather

from src.schemas import QueryRequest, QueryResponse, WikiRequest
from src.graph import build_graph

from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse, StreamingResponse
from src import tokenizer
from src.wiki import (WikiError, NotWikipediaURL, WikiPageNotFound, NoFormulaFound, WikiFetchFailed)
from src.wiki import get_title, get_latex
from src.tokenizer import (TokenizerError, TokenizeUnavailable)
from src.tokenizer import RAW_FORMULAS, WIKI_SECTIONS

load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    langfeather.configure(endpoint="http://127.0.0.1:4319")
    app.state.graph = build_graph()
    yield

app = FastAPI(lifespan=lifespan)

# 시간 상 스트리밍은 내가 이해하고 다시 직접 써보는걸로

# 프론트가 답변 본문과 sources를 구분할 때 쓰는 구분자.
# (사람이 실제로 쓸 만한 문자열은 아니니 답변 본문과 안 겹칠 거라고 가정)
SOURCES_MARKER = "\n\n[[SOURCES]]"

@app.post("/query")
async def query(req: QueryRequest):
    input_state = {
        "messages": [],
        "symbol": req.symbol,
        "context": req.context,
        "page_title": req.page_title,
        "question": req.question,
        "documents": "",
        "sources": [],
        "tool_call": False,
        "full_formula": req.full_formula,
        "source_url": req.source_url,
    }
    config = {"configurable": {"thread_id": req.thread_id}}

    def chunk_text(content) -> str:
        # ChatGoogleGenerativeAI가 가끔 content를 문자열이 아니라
        # [{"type": "text", "text": "..."}] 같은 파츠 리스트로 줄 때가 있어서 방어적으로 문자열화.
        if isinstance(content, str):
            return content
        if isinstance(content, list):
            parts = []
            for part in content:
                if isinstance(part, str):
                    parts.append(part)
                elif isinstance(part, dict):
                    parts.append(part.get("text", ""))
            return "".join(parts)
        return ""

    async def event_stream():
        sources: list[str] = []
        try:
            # stream_mode="messages": generate 노드 안 LLM이 토큰 만들 때마다 (chunk, metadata) 하나씩 나옴.
            # stream_mode="updates": 노드 하나 끝날 때마다 그 노드가 반환한 state 조각이 나옴 (sources 여기서 챙김).
            async for mode, data in app.state.graph.astream(
                input_state, config=config, stream_mode=["messages", "updates"]
            ):
                if mode == "messages":
                    chunk, metadata = data
                    text = chunk_text(chunk.content)
                    if metadata.get("langgraph_node") == "generate" and text:
                        yield text
                elif mode == "updates":
                    retrieve_output = data.get("retrieve")
                    if retrieve_output and retrieve_output.get("sources"):
                        sources = retrieve_output["sources"]
        except Exception as e:
            yield f"\n\n[오류: {e}]"
        yield SOURCES_MARKER + json.dumps(sources, ensure_ascii=False)

    return StreamingResponse(event_stream(), media_type="text/plain")

@app.post("/wiki")
def add_wiki(req: WikiRequest):
    sections, wikitext = get_latex(req.url)
    title = "[Wiki] " + get_title(req.url)[0]
    WIKI_SECTIONS[title] = {"url": req.url, "sections": sections, "wikitext": wikitext}
    return {"title": title}

STATUS = {
    NotWikipediaURL: 400,
    WikiPageNotFound: 404,
    NoFormulaFound: 404,
    TokenizeUnavailable: 501,
    WikiFetchFailed: 502,
}

@app.exception_handler(WikiError)
def handle_wiki_error(request, exc: WikiError):
    return JSONResponse(
        status_code=STATUS.get(type(exc), 500),
        content={"detail": str(exc)},
    )

@app.exception_handler(TokenizerError)
def handle_wiki_error(_, exc: TokenizerError):
    return JSONResponse(
        status_code=STATUS.get(type(exc), 500),
        content={"detail": str(exc)},
    )

@app.get("/page/{title}")
def page(title: str):
    try:
        result = tokenizer.get_page(title)
    except KeyError:
        raise HTTPException(status_code=404, detail=f"페이지 없음: {title}")
    return {"title": title, **result}

@app.get("/pages")
def pages():
    return sorted(list(RAW_FORMULAS) + list(WIKI_SECTIONS))

app.mount("/", StaticFiles(directory="static", html=True), name="static")