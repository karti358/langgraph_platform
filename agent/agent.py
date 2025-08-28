from langgraph.graph import StateGraph, START, END
from langchain_openai import ChatOpenAI
from langchain_community.tools import DuckDuckGoSearchRun
from langsmith import traceable
from langsmith.utils import LangSmithConflictError
import os
import ssl
import urllib3
import certifi

# Disable SSL warnings and verification for DuckDuckGo
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Set SSL environment variables
os.environ['SSL_CERT_FILE'] = certifi.where()
os.environ['REQUESTS_CA_BUNDLE'] = certifi.where()
os.environ['CURL_CA_BUNDLE'] = certifi.where()

# Alternative: Apply SSL fix
try:
    import sys
    sys.path.append('..')
    from ssl_fix import *
except ImportError:
    pass

os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = "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"
os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"
os.environ["LANGCHAIN_PROJECT"] = "comparison-agent"

from langsmith import Client

# Connect to LangSmith
ls_client = Client()


dataset_name = "comparison-dataset"

try:
    dataset = ls_client.create_dataset(
        dataset_name=dataset_name,
        description="Dataset for comparing tools and exporting PDF reports"
    )
except LangSmithConflictError:
    dataset = ls_client.read_dataset(dataset_name=dataset_name)

dataset_id = dataset.id

class State(dict):
    query: str
    comparison: str

graph = StateGraph(State)
from langchain_google_genai import ChatGoogleGenerativeAI

llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    google_api_key="AIzaSyA2qfq6A4wgQfrilYcFvmwbzoVeGica1oA",
    temperature=0.3
)

# Configure DuckDuckGo search with SSL handling
import ssl
import certifi

# Create SSL context that uses system certificates
ssl_context = ssl.create_default_context(cafile=certifi.where())
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

# Initialize search tool
# search_tool = DuckDuckGoSearchRun()

# @traceable
# def web_search(state: State):
#     query = state.get("query", "")
#     try:
#         # Set environment variables for this specific search
#         old_verify = os.environ.get('CURL_CA_BUNDLE')
#         os.environ['CURL_CA_BUNDLE'] = certifi.where()
        
#         # Use DuckDuckGo search with error handling
#         results = search_tool.run(query)
#         state["search_results"] = results
        
#         # Restore original environment
#         if old_verify:
#             os.environ['CURL_CA_BUNDLE'] = old_verify
            
#     except Exception as e:
#         # Fallback: provide a message about search failure but continue processing
#         fallback_message = f"""
#         Note: Web search encountered SSL/network issues. 
#         Proceeding with query analysis based on the original query: "{query}"
        
#         Error details: {str(e)}
#         """
#         state["search_results"] = fallback_message
#         print(f"Search error: {e}")
    
#     return state

@traceable
def compare_results(state: State):
    query = state['query']
    
    prompt = f"""
    Compare the following products/tools based on the search results:

    Query: {query}

    Give me a structured comparison (features, pros, cons, summary). In neat and clean format so that it can be directly used in a PDF report.
    """
    
    response = llm.invoke(prompt)
    state["comparison"] = response.content
    return state


# graph.add_node("search", web_search)
graph.add_node("compare", compare_results)

# graph.add_edge(START, "search")
# graph.add_edge("search", "compare")
graph.add_edge(START, "compare")
graph.add_edge("compare", END)

app = graph.compile()

@traceable
def run_graph(query: str):
    return app.invoke({"query": query})