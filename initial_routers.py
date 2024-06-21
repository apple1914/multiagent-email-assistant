from typing import Literal
from graph_state import GraphState

def route_to_workflow(
    state: GraphState,
) -> Literal[
    "assistant_one",
]:
    """If we are in a delegated state, route directly to the appropriate assistant."""
    dialog_state = state.get("dialog_state")
    if not dialog_state:
        return "assistant_one"
    return dialog_state

def restream_message(state:GraphState):
    dialog_state = state.get("dialog_state")
    assistant_name = dialog_state
    if not dialog_state:
        assistant_name = "assistant_one"
    last_user_message = state.get("last_user_message")
    
    # message = HumanMessage(last_user_message)
    return {assistant_name+"_messages":[{"role":"user","content":last_user_message}]}

