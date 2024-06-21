from typing import Literal
from graph_state import GraphState





def tools_condition_edge(assistant_name,state) -> Literal["assistant", "tools", "__end__"]:
    # print("messages",messages)
    messages = state[assistant_name+"_messages"]
    last_message = messages[-1]
    if type(last_message["tool_calls"]) is list and len(last_message["tool_calls"]) > 0:
        return "tools"
    elif last_message["role"] == 'assistant':
        return "__end__"
    else:
        return "assistant"