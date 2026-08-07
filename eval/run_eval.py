# 기능보다 엔지니어링적인 해결 방법
# 실시간?

import json
from src.graph import build_graph
from eval.metrics.rest_metric import ff_metric, cp_metric, cr_metric
from eval.metrics.geval_metric import se_metric, ar_metric, ne_metric
from langchain_core.messages import ToolMessage
import langfeather

from deepeval.test_case import LLMTestCase
from deepeval import evaluate

import re, time
from langchain_google_genai.chat_models import ChatGoogleGenerativeAIError

with open('./eval/datasets/general_QA.json', 'r', encoding='utf-8') as file:
    general_questions = json.load(file)

with open('./eval/datasets/symbol_QA.json', 'r', encoding='utf-8') as file:
    symbol_questions = json.load(file)

total_questions = general_questions + symbol_questions
llm_questions = symbol_questions[-5:]
infer_questions = [item for item in total_questions if "answer" in item]
no_infer_questions = [item for item in total_questions if "answer" not in item]

langfeather.configure(endpoint="http://127.0.0.1:4319")
eval_graph = build_graph()
groups = {}

class DeepEvalError(Exception): pass

def invoke_with_retry(graph, state, config, max_attempts=3):
    for attempt in range(max_attempts):
        try:
            return graph.invoke(state, config=config)
        except ChatGoogleGenerativeAIError as e:
            if "429" not in str(e) or attempt == max_attempts - 1:
                raise
            match = re.search(r"retry_delay\s*\{\s*seconds:\s*(\d+)", str(e))
            delay = int(match.group(1)) if match else 60
            print(f"  429 — {delay}초 대기 후 재시도")
            time.sleep(delay)

def evaluate_with_retry(test_cases, metrics, max_attempts=3):
    for attempt in range(max_attempts):
        try:
            return evaluate(test_cases=test_cases, metrics=metrics)
        except Exception as e:
            if attempt == max_attempts - 1:
                print(f"  [그룹 평가 실패, 건너뜀] {type(e).__name__}: {e}")
                return None
            print(f"  재시도 {attempt + 1}/{max_attempts}...")
            time.sleep(3)

failed = []
collected = []
for idx, case in enumerate(total_questions):
    print(f"[{idx + 1}/{len(total_questions)}] {case.get('question') or case.get('symbol')}")
    try:
        case_state = {
            "messages": [],
            "symbol": "",
            "context": "",
            "page_title": case["page_title"], # JSON 항목에서 가져와야 하는 상황
            "question": "",
            "documents": "",
            "sources": [],
            "tool_call": False,
            "full_formula": "",
            "source_url": "",
        }

        if case in symbol_questions:
            case_state["symbol"] = case["symbol"]
            case_state["context"] = case["context"]
            case_state["full_formula"] = case["full_formula"]
        else:
            case_state["question"] = case["question"]

        try:
            result = invoke_with_retry(
                eval_graph, 
                case_state, 
                config={"configurable": {"thread_id": f"eval-{idx}"}}, 
                max_attempts=3
            )
        except Exception as e:
            print(f"[{idx}] FAILED: {e}")
            failed.append(idx)
        else:
            retrieval_chunk = [result["documents"]]
            tool_chunks = [
                msg.content for msg in result["messages"] 
                if isinstance(msg, ToolMessage)
            ]

            if result["tool_call"]:
                retrieval_chunk = retrieval_chunk + tool_chunks

            metric_list = [ff_metric, ne_metric] # cr_metric, 
            if case in symbol_questions:
                metric_list.append(se_metric)
                if case in llm_questions:
                    metric_list.remove(ff_metric)
                    # metric_list.remove(cr_metric)

            if case in infer_questions:
                metric_list = metric_list + [ar_metric] # cp_metric, 
                # 내가 보기엔 여기에 이제 기호에 대한 index 같은 것도 넣어야 할 것 같아

            test_case = LLMTestCase(
                input=result["question"],
                actual_output=result["messages"][-1].text,
                expected_output=case.get("answer"),
                retrieval_context=retrieval_chunk,
            )
            """
            key = tuple(m.__name__ for m in metric_list)
            groups.setdefault(key, {"metrics": metric_list, "test_cases": []})
            groups[key]["test_cases"].append(test_case)
            """
            expected_tool = case.get("expect_tool")
            if expected_tool is not None:
                ok = (result["tool_call"] == expected_tool)
                print(f"  라우팅 {'OK' if ok else 'FAIL'} (기대 {expected_tool}, 실제 {result['tool_call']})")

            collected.append((test_case, metric_list))
            
    except Exception as e:
        print(f"[{idx}] FAILED: {e}")
        failed.append(idx)

"""
for group in groups.values():
    final_result = evaluate_with_retry(test_cases=group["test_cases"], metrics=group["metrics"])
    if final_result is None:
        continue
    for test_result in final_result.test_results:
        for metric_data in test_result.metrics_data:
            print(metric_data.name, metric_data.score, metric_data.threshold)
            print(metric_data.reason)
            print("---")
"""

for tc, metrics in collected:
    for m in metrics:
        try:
            m.measure(tc)
            print(m.__class__.__name__, m.score)
            print(m.reason)
        except Exception as e:
            print(f"  [지표 실패] {type(e).__name__}: {e}")
        print("---")

langfeather.flush(timeout=2)