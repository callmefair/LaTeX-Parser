from pydantic import BaseModel, Field

class QueryRequest(BaseModel):
    symbol: str = ""
    context: str = ""
    page_title: str = ""
    question: str = ""
    thread_id: str = "DEFAULT"
    full_formula: str = ""
    source_url: str = ""

class QueryResponse(BaseModel):
    answer: str = ""
    sources: list[str] = []

class WikiRequest(BaseModel):
    url: str
