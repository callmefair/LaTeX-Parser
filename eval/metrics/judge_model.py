from deepeval.models import AnthropicModel
from src.config import ANTHROPIC_MODEL, ANTHROPIC_API_KEY

judge_llm = AnthropicModel(
    model=ANTHROPIC_MODEL,
    api_key=ANTHROPIC_API_KEY,
    generation_kwargs={"max_tokens": 4096},
)