from fastapi import FastAPI
from pydantic import BaseModel

from generate import generate_reply, load_model

app = FastAPI(title="한국어 챗봇 (Char-level Transformer LM)")

# 서버 시작 시 한 번만 모델 로딩 (요청마다 다시 불러오면 매우 느려짐)
model, tokenizer, device = load_model()


class ChatRequest(BaseModel):
    message: str
    temperature: float = 0.8
    max_new_tokens: int = 60


class ChatResponse(BaseModel):
    reply: str


@app.get("/")
def root():
    return {"status": "ok", "usage": "POST /chat {\"message\": \"안녕\"}"}


@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    reply = generate_reply(
        model, tokenizer, device, req.message,
        max_new_tokens=req.max_new_tokens,
        temperature=req.temperature,
    )
    return ChatResponse(reply=reply)
