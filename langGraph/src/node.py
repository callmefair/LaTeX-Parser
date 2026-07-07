from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_google_genai import ChatGoogleGenerativeAI
 
from src.config import GOOGLE_MODEL, GOOGLE_API_KEY
from src.retriever import get_retriever
from src.tools import TOOLS

retriever = get_retriever()

llm = ChatGoogleGenerativeAI(
    model=GOOGLE_MODEL,
    google_api_key=GOOGLE_API_KEY,
).bind_tools(TOOLS)

def route(state) -> str:
    return "symbol_question" if state["symbol"] else "passthrough"

def symbol_question(state) -> dict:
    question = f"${state["symbol"]}$이 ${state["context"]}$에서 사용됐습니다. 현재 페이지: {state["page_title"]}. 기호에 대해서 설명해주세요."
    return {"question": question}

def passthrough(state) -> dict:
    return {}
    # 한 줄로 할 수 있을 것 같음에도 불구하고 LangGraph 감 좀 잡아보려고 나눠봤음

def query(state) -> dict:
    return {"messages": state["question"]}
    # 우리는 question이 두 가지 갈래에서 오니까 state["messages"][-1].content 안 쓰고 question 따로 분리

def retrieve(state) -> dict:
    docs = retriever.invoke(state["question"])
    sources = []
    contents = []
    for doc in docs:
        sources.append(doc.metadata["source"])
        contents.append(doc.page_content)
    formatted = "\n\n".join(contents)

    unique_sources = list(dict.fromkeys(sources))

    return {
        "documents": formatted,
        "sources": unique_sources,
    }

def generate(state) -> dict:
    prompt = ChatPromptTemplate.from_messages([
        ("system",
        "당신은 수학 기호와 개념을 설명하는 전문가입니다. "
        "다음 문서를 근거로 사용자 질문에 답하세요. "
        "문서에 근거가 부족하면 wiki_search 도구를 사용하세요. \n\n"
        "{documents}"),
        MessagesPlaceholder(variable_name="messages"),
    ])
    # 이미 질문이 맨 뒤에 있어서 "human"을 따로 안 붙인 케이스
    # 어떻게든 "human" 만들어서 eval 만드는 것도 방법일지도!!

    chain = prompt | llm
    response = chain.invoke(state)

    return {"messages": [response]}