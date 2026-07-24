import json
from src.graph import build_graph
from metrics.rest_metric import ff_metric, cp_metric, cr_metric
from metrics.geval_metric import se_metric
from langchain_core.messages import ToolMessage

from depeval.test_case import LLMTestCase
from deepeval.dataset import EvaluationDataset
from deepeval import evaluate

with open('./datasets/general_QA.json', 'r', encoding='utf-8') as file:
    general_questions = json.load(file)

with open('./datasets/symbol_QA.json', 'r', encoding='utf-8') as file:
    symbol_questions = json.load(file)

total_questions = general_questions + symbol_questions
infer_questions = [item for item in total_questions if "answer" in item]
no_infer_questions = total_questions - infer_questions # JSON 항목을 수정해야 하는 사항

eval_graph = build_graph()
test_cases = []

for case in total_questions:
    case_state = {
        "messages": [],
        "symbol": "",
        "context": "",
        "page_title": case["page_title"], # JSON 항목에서 가져와야 하는 상황
        "question": case["question"],
        "documents": "",
        "sources": [],
        "tool_call": False,
    }

    if case in symbol_questions:
        case_state["symbol"] = case["symbol"]
        case_state["context"] = case["context"] # JSON 항목에서 가져와야 하는 상황

    result = eval_graph.invoke(case_state)

    retrieval_chunk = [result["documents"]]
    tool_chunks = [
        msg.content for msg in result["messages"] 
        if isinstance(msg, ToolMessage)
    ]

    if result["tool_call"]:
        retrieval_chunk = retrieval_chunk + tool_chunks

    if case in no_infer_questions:
        test_case = LLMTestCase(
            input=case["question"],
            actual_output=result["messages"][-1].text,
            retrieval_context=retrieval_chunk,
            metrics=[ff_metric, cr_metric],
        )
    else:
        test_case = LLMTestCase(
            input=case["question"],
            actual_output=result["messages"][-1].text,
            retrieval_context=retrieval_chunk,
            metrics=[cp_metric],
        ) # 아직 geval_metric.py 미완성 + cp_metric

    test_cases.append(test_case)

combined_dataset = EvaluationDataset(test_cases=test_cases)
evaluate(combined_dataset)

"""
import re

def check_latex_syntax(text: str) -> bool:
    # LaTeX 달러 기호($$)의 짝이 맞는지 검사하는 간단한 정규식 테스트
    # Inline $ 짝 검사
    inline_dollars = len(re.findall(r'(?<!\\)\$', text))
    if inline_dollars % 2 != 0:
        return False
    # KaTeX 에러 문자열 존재 여부 검사 등
    if "KaTeX parse error" in text:
        return False
    return True
"""