from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI

from src.schemas import QueryRequest, QueryResponse
from src.graph import build_graph

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