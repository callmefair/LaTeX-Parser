from deepeval.metrics import FaithfulnessMetric, ContextualPrecisionMetric, ContextualRelevancyMetric

from langchain_anthropic import ChatAnthropic
from src.config import ANTHROPIC_MODEL, ANTHROPIC_API_KEY

judge_llm = ChatAnthropic(
    model=ANTHROPIC_MODEL,
    api_key=ANTHROPIC_API_KEY
)

#Faithfulness
ff_metric = FaithfulnessMetric(
    threshold=0.5,
    model=judge_llm,
    include_reason=True
)
# 답변이. Context 역할을 하는 것의 기반인가? 툴 호출에 따라 다르게 하는게 있는지 확인해봐야 할지도?

#ContextualPrecision
cp_metric = ContextualPrecisionMetric(
    threshold=0.5,
    model=judge_llm,
    include_reason=True
)
# Retriever가 가져온 청크가 상위에 왔는가?

#ContextualRelevancy
cr_metric = ContextualRelevancyMetric(
    threshold=0.5,
    model=judge_llm,
    include_reason=True
)
# Retriever가 가져온 청크가 질문과 관련이 있는가?