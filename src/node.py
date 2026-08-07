from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_google_genai import ChatGoogleGenerativeAI
 
from src.config import GOOGLE_MODEL, GOOGLE_API_KEY
from src.retriever import get_retriever
from src.tools import TOOLS
from langchain_core.messages import ToolMessage
from src.prompt import SYMBOL_PROMPT, GENERAL_PROMPT

from src.tokenizer import WIKI_SECTIONS, find_symbol_lines

retriever = get_retriever()

llm_with_tools = ChatGoogleGenerativeAI(
    model=GOOGLE_MODEL,
    google_api_key=GOOGLE_API_KEY,
).bind_tools(TOOLS)

llm_no_tools = ChatGoogleGenerativeAI(
    model=GOOGLE_MODEL,
    google_api_key=GOOGLE_API_KEY,
)

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
    formatted = "[내 노트에서 검색된 내용]\n" + "\n\n".join(contents)
    unique_sources = list(dict.fromkeys(sources))

    if state["symbol"] and state["page_title"] in WIKI_SECTIONS and state["symbol"] not in formatted:
        extra = find_symbol_lines(state["page_title"], state["symbol"])
        if extra:
            formatted = "\n\n[문서 원문에서 찾은 해당 기호의 용례]\n\n" + "\n\n".join(extra)
            unique_sources.append(state["page_title"])
    
    return {
        "documents": formatted,
        "sources": unique_sources,
    }

def generate(state) -> dict:
    if state["symbol"]:
        prompt = ChatPromptTemplate.from_messages([
            ("system", SYMBOL_PROMPT), 
            MessagesPlaceholder(variable_name="messages")
        ])
        chain = prompt | llm_no_tools
    else:
        prompt = ChatPromptTemplate.from_messages([
            ("system", GENERAL_PROMPT), 
            MessagesPlaceholder(variable_name="messages")
        ])
        chain = prompt | llm_with_tools
    # 이미 질문이 맨 뒤에 있어서 "human"을 따로 안 붙인 케이스
    # 어떻게든 "human" 만들어서 eval 만드는 것도 방법일지도!!

    used_tool = state.get("tool_call", False) or isinstance(
        state["messages"][-1], ToolMessage
    ) if state["messages"] else False

    response = chain.invoke(state)

    return {"messages": [response], "tool_call": used_tool}