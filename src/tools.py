from langchain_core.tools import tool
from langchain_community.document_loaders import WikipediaLoader

@tool
def wiki_search(query: str) -> str:
    """로컬 문서에 없는 수학 개념/기호를 영어 위키피디아에서 검색한다.
    로컬 검색 결과가 질문에 답하기에 부족할 때만 사용하라.
    쿼리는 서술형 문장이 아닌 위키피디아 문서 제목에 가까운 정확한 수학 용어로 작성하라."""
    try:
        loader = WikipediaLoader(query=query, lang="en", load_max_docs=3)
        docs = loader.load()
        return "\n\n".join(doc.page_content for doc in docs)
    except Exception as e:
        return f"위키피디아 검색 실패: {e}. 검색 없이 아는 범위에서 답하거나, 실패했다고 사용자에게 알려라."

TOOLS = [wiki_search]

"""
@tool
def wiki_search(query: list[str]) -> str:
    로컬 문서에 없는 수학 개념/기호를 영어 위키피디아에서 검색한다.
    로컬 검색 결과가 질문에 답하기에 부족할 때만 사용하라.
    docs = []
    for topic in query:
        loader = WikipediaLoader(query=topic, lang="en", load_max_docs=3)
        docs.extend(loader.load())
    return "\n\n".join(docs)
"""