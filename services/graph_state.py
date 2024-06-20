
from typing import Annotated, TypedDict

from langgraph.graph.message import add_messages

class GraphState(TypedDict):
    """
    Represents the state of our graph.

    Attributes:
        dialogue_state: str
        messages: list
        name:str
    """

    messages: Annotated[list, add_messages]
    dialogue_state: str   #which agent the user was talking to last
    name:str #placeholder for info about user's context, such as their about me or value prop if it's a company
    