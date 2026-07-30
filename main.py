from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException

from src.schemas import QueryRequest, QueryResponse
from src.graph import build_graph

from fastapi.staticfiles import StaticFiles
from src import tokenizer

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

@app.get("/page/{title}")
def page(title: str):
    try:
        result = tokenizer.get_page(title)
    except KeyError:
        raise HTTPException(status_code=404, detail=f"페이지 없음: {title}")
    return {"title": title, **result}

@app.get("/pages")
def pages():
    return sorted(tokenizer.RAW_FORMULAS.keys())

app.mount("/", StaticFiles(directory="static", html=True), name="static")