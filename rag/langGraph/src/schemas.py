from pydantic import BaseModel

class QueryRequest(BaseModel):
    symbol: str = ""
    context: str = ""
    page_title: str = ""
    question: str = ""
    thread_id = "DEFAULT"

class QueryResponse(BaseModel):
    answer: str = ""
    sources: list[str] = []