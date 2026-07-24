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

class MetricScore(BaseModel):
    score: float = Field(
        ge=0.0,
        le=1.0,
        # description
    )
    reasoning: str = Field(description="점수의 핵심 근거를 한국어로 간결하게 설명. 1~2 문장으로 간단하게 서술하세요.")
    
