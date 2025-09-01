from langchain_anthropic import ChatAnthropic
from typing import Annotated, Sequence, TypedDict, Any
from langchain_core.messages import (
    BaseMessage,
    SystemMessage,
    HumanMessage,
)
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, END
from langchain_core.tools import tool
from langchain_core.documents import Document
from ddgs import DDGS
from langgraph.prebuilt import ToolNode
from langchain_voyageai import VoyageAIEmbeddings
from dotenv import load_dotenv

import os
from langchain_community.retrievers import KNNRetriever

load_dotenv()


# TODO: Move this to a schema eventually
class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]
    # messages: List[Union[HumanMessage, AIMessage, SystemMessage]]


embeddings = VoyageAIEmbeddings(
    voyage_api_key=os.getenv("VOYAGE_API_KEY"),
    model="voyage-law-2",  # type: ignore
)  # type: ignore

documents = [
    "Diversification is an investment strategy that involves spreading your investments across various asset classes, such as stocks, bonds, and real estate, to reduce risk. By not putting all your money into one type of investment, you can help protect your portfolio from significant losses if one investment performs poorly.",
]

documents_embds = embeddings.embed_documents(documents)

retriever = KNNRetriever.from_texts(documents, embeddings)


@tool
def search_on_internal_knowledge(query: str) -> list[Document]:
    """Search on internak knowledge base

    Args:
        query: The question you want to send look on the internet
    """
    # print("Looking for information on our internal knowledge base")
    result = retriever.invoke(query)
    return result


@tool
def search_on_ddg(query: str) -> list[dict[str, Any]]:
    """Search on the internet any question you might have

    Args:
        query: The question you want to send look on the internet
    """
    # print("starting search")
    # TODO: find a way to query DDG async
    results = DDGS().text(query, max_results=5)
    # print(results)

    return results


tools = [search_on_internal_knowledge, search_on_ddg]


model = ChatAnthropic(
    model="claude-3-7-sonnet-20250219",  # type: ignore
    temperature=0,
    max_tokens=1024,  # type: ignore
).bind_tools(tools)


def start_agent(state: AgentState) -> AgentState:
    # print("Hello there!")
    system_prompt = SystemMessage(
        content="""
        You are a helpful writing assistant. You are going to answer the user questions.
        First, you gonna search in our internal knowledge using the tool search_on_internal_knowledge.
        If you do not find any relevant information, You gonna use external search tool to search on the internet if you need the information
        """
    )
    response = model.invoke([system_prompt] + state["messages"])  # type: ignore
    return {"messages": [response]}


def should_continue(state: AgentState) -> str:
    message = state["messages"]
    last_message = message[-1]
    if not last_message.tool_calls:  # type: ignore
        # print("end should continue")
        return "end"
    else:
        # print("continue should continue")
        return "continue"


def return_agent_answer(question: str) -> str:
    graph = StateGraph(AgentState)
    graph.add_node("process", start_agent)
    tool_node = ToolNode(tools=tools)
    graph.add_node("tools", tool_node)
    graph.set_entry_point("process")
    graph.add_conditional_edges(
        "process", should_continue, {"continue": "tools", "end": END}
    )
    graph.add_edge("tools", "process")
    agent = graph.compile()

    user_question = HumanMessage(content=question)

    result = agent.invoke({"messages": [user_question]})

    return (
        result["messages"][-1].pretty_repr()
    )  # TODO: Find a way to only get the answer without the "AI MESSAGE" header
