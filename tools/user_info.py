from langchain_core.tools import tool
from services.graph_state import GraphState
@tool
def fetch_customer_info() -> str:
    "fetch this persons name"
    # this is not implemented yet, but later on I can use this to fetch context about the user, i.e. if they are looking for a job or they're selling something etc, as prsets saved in our db
    return "eleke"
def user_info_node(state: GraphState):
    return {"name": fetch_customer_info.invoke({})}