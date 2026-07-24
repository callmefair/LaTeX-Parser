# 선행 조건: md 파일이 바뀔 때마다 uv run python -m scripts.ingest 실행

from src.retriever import get_retriever
from src.config import RETRIEVER_K

def test_retriever_k_docs():
    docs = get_retriever().invoke("Central Limit Theorem")
    assert len(docs) == RETRIEVER_K
    print("앞 200글자: ", docs[0].page_content[:200])
    assert "source" in docs[0].metadata

from src.node import retrieve
def test_node_to_retrieve():
    out = retrieve({"question": "Central Limit Theorem이 뭐야?"})
    print("출처: ", out["sources"])
    print("앞 200글자: ", out["documents"][:200])
    # retrieve 함수의 return에 있는 것을 확인하면 돼

from src.node import generate
def test_generate_no_tools():
    out = retrieve({"question": "Central Limit Theorem이 뭐야?"})
    result = generate({
        "documents": out["documents"],
        "messages": [("human", "Central Limit Theorem이 뭐야?")],
    })
    # generate 함수가 필요로 하는 것들을 retrieve의 결과와
    # "messages"가 "question"으로부터 만들어졌다고 가정하고
    print("대답: ", result["messages"][0].content)
    assert result["messages"][0].tool_calls == []
    # graph.py가 연결되기 전까지는 generate의 결과물은 {"messages": [response]} 그 자체
    # 우리가 아는 concatenate는 add_messages가 해주는거야! 그러니 [0]을 불러야 해
    # 아무튼 tool_calls가 0이여야겠지. 로컬 문서의 것을 가져왔으니

def test_generate_use_tools():
    result = generate({
        "documents": "관련 문서 없음",
        "messages": [("human", "Banach-Tarski paradox가 뭐야?")],
    })
    assert result["messages"][0].tool_calls[0]["name"] == "wiki_search"
    # tool_calls 결과 기대

from src.graph import build_graph
def test_visualize():
    g = build_graph()
    print(g.get_graph().draw_mermaid())
    print("결과를 복사해서 옵시디언 mermaid 코드 블럭에 넣으시오.")

def test_graph_works():
    g = build_graph()
    out = g.invoke(
        {"symbol": "", "context": "", "page_title": "", "question": "CLT가 뭐야?"},
        config={"configurable": {"thread_id": "test-1"}},
    )
    print(out["messages"][-1].text)
    # 여기의 "messages"는 정말로 add_message로 이어진 list