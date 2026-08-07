from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode, tools_condition
from typing import Annotated, TypedDict
from langgraph.graph.message import add_messages

from src.node import route, symbol_question, passthrough, query, retrieve, generate
from src.tools import TOOLS

from langgraph.checkpoint.memory import InMemorySaver
import langfeather

class State(TypedDict):
    messages: Annotated[list, add_messages]
    symbol: str
    context: str
    page_title: str
    question: str
    documents: str
    sources: list[str]
    tool_call: bool
    full_formula: str
    source_url: str

def build_graph():
    graph = StateGraph(State)
    graph.add_node("symbol_question", symbol_question)
    graph.add_node("passthrough", passthrough)
    graph.add_node("query", query)
    graph.add_node("retrieve", retrieve)
    graph.add_node("generate", generate)
    graph.add_node("tools", ToolNode(tools=TOOLS))

    graph.add_conditional_edges(START, route, ["symbol_question", "passthrough"])
    graph.add_edge("symbol_question", "query")
    graph.add_edge("passthrough", "query")
    graph.add_edge("query", "retrieve")
    graph.add_edge("retrieve", "generate")
    graph.add_conditional_edges(
        "generate",
        tools_condition,
        {
            "tools": "tools",
            "__end__": END,
        },
    )
    graph.add_edge("tools", "generate")

    compiled = graph.compile(checkpointer=InMemorySaver())
    return langfeather.wrap_runnable(compiled, name="latex-parser")