# 기능보다 엔지니어링적인 해결 방법
# 실시간?

import json
from src.graph import build_graph
from eval.metrics.rest_metric import ff_metric, cp_metric, cr_metric
from eval.metrics.geval_metric import se_metric, ar_metric, ne_metric
from langchain_core.messages import ToolMessage

from deepeval.test_case import LLMTestCase
from deepeval import evaluate

import re, time
from langchain_google_genai.chat_models import ChatGoogleGenerativeAIError

with open('./eval/datasets/general_QA.json', 'r', encoding='utf-8') as file:
    general_questions = json.load(file)

with open('./eval/datasets/symbol_QA.json', 'r', encoding='utf-8') as file:
    symbol_questions = json.load(file)

total_questions = general_questions + symbol_questions
infer_questions = [item for item in total_questions if "answer" in item]
no_infer_questions = [item for item in total_questions if "answer" not in item]

eval_graph = build_graph()
groups = {}

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

failed = []
for idx, case in enumerate(total_questions[:3]):
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
        }

        if case in symbol_questions:
            case_state["symbol"] = case["symbol"]
            case_state["context"] = case["context"]
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

            metric_list = []

            if case in no_infer_questions:
                metric_list = metric_list + [ff_metric, cr_metric, ne_metric]
                if case in symbol_questions:
                    metric_list.append(se_metric)
            else:
                metric_list = metric_list + [cp_metric, ar_metric]
                # 내가 보기엔 여기에 이제 기호에 대한 index 같은 것도 넣어야 할 것 같아

            test_case = LLMTestCase(
                input=result["question"],
                actual_output=result["messages"][-1].text,
                expected_output=case.get("answer"),
                retrieval_context=retrieval_chunk,
            )

            key = tuple(m.__name__ for m in metric_list)
            groups.setdefault(key, {"metrics": metric_list, "test_cases": []})
            groups[key]["test_cases"].append(test_case)

            
    except Exception as e:
        print(f"[{idx}] FAILED: {e}")
        failed.append(idx)

for group in groups.values():
    final_result = evaluate(test_cases=group["test_cases"], metrics=group["metrics"])
    for test_result in final_result.test_results:
        for metric_data in test_result.metrics_data:
            print(metric_data.name, metric_data.score, metric_data.threshold)
            print(metric_data.reason)
            print("---")