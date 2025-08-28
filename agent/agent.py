from langgraph.graph import StateGraph, START, END
from langchain_openai import ChatOpenAI
from langchain_community.tools import DuckDuckGoSearchRun
from langsmith import traceable
from langsmith.utils import LangSmithConflictError
import os

os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = "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"
os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"
os.environ["LANGCHAIN_PROJECT"] = "comparison-agent"

class State(dict):
    query: str
    search_results: str
    comparison: str

graph = StateGraph(State)
from langchain_google_genai import ChatGoogleGenerativeAI

llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    google_api_key="AIzaSyA2qfq6A4wgQfrilYcFvmwbzoVeGica1oA",
    temperature=0.3
)

search_tool = DuckDuckGoSearchRun()

@traceable
def web_search(state: State):
    query = state.get("query", "")
    results = search_tool.run(query)
    state["search_results"] = results
    return state

@traceable
def compare_results(state: State):
    prompt = f"""
    Compare the following products/tools based on the search results:

    Query: {state['query']}
    Results: {state['search_results']}

    Give me a structured comparison (features, pros, cons, summary). In neat and clean fromat so that it can be directly used in a PDF report.
    """
    response = llm.invoke(prompt)
    state["comparison"] = response.content
    return state


graph.add_node("search", web_search)
graph.add_node("compare", compare_results)

graph.add_edge(START, "search")
graph.add_edge("search", "compare")
graph.add_edge("compare", END)

app = graph.compile()

@traceable
def run_graph(query: str):
    return app.invoke({"query": query})
