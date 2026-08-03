from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException

from src.schemas import QueryRequest, QueryResponse, WikiRequest
from src.graph import build_graph

from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from src import tokenizer
from src.wiki import (WikiError, NotWikipediaURL, WikiPageNotFound, NoFormulaFound, WikiFetchFailed)
from src.wiki import get_title, get_latex
from src.tokenizer import (TokenizerError, TokenizeUnavailable)
from src.tokenizer import WIKI_SECTIONS, tokenize_sections

load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.graph = build_graph()
    yield

app = FastAPI(lifespan=lifespan)

@app.post("/query", response_model=QueryResponse)
def query(req: QueryRequest):
    result = app.state.graph.invoke(
        {
            "messages": [],
            "symbol": req.symbol,
            "context": req.context,
            "page_title": req.page_title,
            "question": req.question,
            "documents": "",
            "sources": [],
            "tool_call": False,
        },
        config = {"configurable": {"thread_id": req.thread_id}},
    )
    return QueryResponse(
        answer=result["messages"][-1].text,
        sources=result["sources"],
        )

@app.post("/wiki")
def add_wiki(req: WikiRequest):
    sections = get_latex(req.url)
    title = "[Wiki] " + get_title(req.url)[0]
    tokenizer.WIKI_SECTIONS[title] = sections
    page = tokenize_sections(sections)
    for s in page["sections"]:
        for f in s["formulas"]:
            if "{\\htmlData}" in f:
                print(f[:200])
                break
    return {"title": title}


STATUS = {
    NotWikipediaURL:  400,
    WikiPageNotFound: 404,
    NoFormulaFound:   404,
    TokenizeUnavailable: 501,
    WikiFetchFailed:  502,
}

@app.exception_handler(WikiError)
def handle_wiki_error(request, exc: WikiError):
    return JSONResponse(
        status_code=STATUS.get(type(exc), 500),
        content={"detail": str(exc)},
    )

@app.exception_handler(TokenizerError)
def handle_wiki_error(request, exc: TokenizerError):
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
    return sorted(list(tokenizer.RAW_FORMULAS) + list(tokenizer.WIKI_SECTIONS))

app.mount("/", StaticFiles(directory="static", html=True), name="static")