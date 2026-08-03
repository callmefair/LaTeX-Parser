from pydantic import BaseModel, Field

class QueryRequest(BaseModel):
    symbol: str = ""
    context: str = ""
    page_title: str = ""
    question: str = ""
    thread_id: str = "DEFAULT"

class QueryResponse(BaseModel):
    answer: str = ""
    sources: list[str] = []

class WikiRequest(BaseModel):
    url: str
