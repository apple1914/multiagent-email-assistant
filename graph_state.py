
from typing import Annotated, TypedDict,Union
# from langgraph.graph.message import add_messages
# from langchain_core.messages import (
#     MessageLikeRepresentation,
# )

# from langgraph.graph.message import add_messages
Messages = Union[list[dict], dict]

def add_objects(left: Messages, right: Messages) -> Messages:
    return left + right

class GraphState(TypedDict):
    """
    Represents the state of our graph.

    Attributes:
        dialogue_state: str
        assistant_one_messages: list
        assistant_two_messages: list
        last_user_message: str
        name:str
    """

    assistant_one_messages: Annotated[list, add_objects]
    assistant_two_messages: Annotated[list, add_objects]
    last_user_message: str 
    dialogue_state: str   #which agent the user was talking to last
    name:str #placeholder for info about user's context, such as their about me or value prop if it's a company
    