from typing import Literal
from langchain_core.messages import AIMessage, HumanMessage
from services.graph_state import GraphState
def from_main_assistant_edge(state) -> Literal["main_assistant_tools_node", "main_assistant", "__end__"]:
    # print("messages",messages)
    messages = state["messages"]
    if isinstance(messages[-1], AIMessage) and messages[-1].tool_calls:
        print("gonna route main assistant to tool_calls")
        return "main_assistant_tools_node"
    elif not isinstance(messages[-1], HumanMessage):
        return END
    return "main_assistant"



def from_evaluator_assistant_edge(state) -> Literal["evaluator_assistant_tools_node", "evaluator_assistant", "__end__"]:
    # print("messages",messages)
    messages = state["messages"]
    if isinstance(messages[-1], AIMessage) and messages[-1].tool_calls:
        thisToolCall = messages[-1].tool_calls[0]
       
        return "evaluator_assistant_tools_node"
    elif not isinstance(messages[-1], HumanMessage):
        return END
    return "evaluator_assistant"

def from_evaluator_assistant_tools_edge(state) -> Literal["main_assistant_entry_node", "__end__"]:
    # print("messages",messages)
    messages = state["messages"]
    tcs = messages[-1].tool_calls
    tc = tcs[0]
    if tc["name"] == "route_to_main_assistant":
        return "main_assistant_entry_node"
    elif tc["name"] == "accept_suggested_company":
        return "__end__"
    else:
        raise ValueError("invalid value for tool call name")

def route_to_workflow(
    state: GraphState,
) -> Literal[
    "main_assistant",
    "evaluator_assistant",
]:
    """If we are in a delegated state, route directly to the appropriate assistant."""
    dialog_state = state.get("dialog_state")
    if not dialog_state:
        return "main_assistant"
    return dialog_state