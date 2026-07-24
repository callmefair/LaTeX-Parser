from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles          # [추가]

from src.schemas import QueryRequest, QueryResponse
from src.graph import build_graph
from src import tokenizer                            # [추가]

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
            "documents": [],
            "sources": [],
        },
        config = {"configurable": {"thread_id": req.thread_id}},
    )
    return QueryResponse(
        answer=result["messages"][-1].text,
        sources=result["sources"],
        )


# [추가] 토큰화된 수식 페이지를 내려주는 엔드포인트.
# 프론트가 화면을 그릴 때 딱 한 번 호출한다. /query와는 완전히 독립.
@app.get("/page/{title}")
def page(title: str):
    try:
        result = tokenizer.get_page(title)
    except KeyError:
        raise HTTPException(status_code=404, detail=f"페이지 없음: {title}")
    return {"title": title, **result}


# [추가] static/index.html 서빙. 브라우저에서 http://localhost:8000/ 접속.
# ※ 라우트 정의보다 반드시 '아래'에 있어야 /query, /page가 가려지지 않음.
app.mount("/", StaticFiles(directory="static", html=True), name="static")
