from contionoal_edges import  tools_condition_edge
from graph_state import GraphState
from langgraph.graph import  StateGraph
from langgraph.checkpoint.sqlite import SqliteSaver

from scraping import parse_page
from openai import OpenAI
from initial_routers import restream_message,route_to_workflow
import json
openai_client = OpenAI()
class BasicTool:
    def __init__(self, callableFunc,name):
        self.callableFunc = callableFunc
        self.name = name

    def invoke(self, inputs: dict):
        print("--------ZAZAZAZA--------")
        print(inputs)
        return self.callableFunc(**inputs)
    
    

class OpenAIAssistant:
    def __init__(self, prompt_text: str, tools_schema:list,assistant_name:str):
        self.prompt_text = prompt_text
        self.tools_schema = tools_schema
        self.assistant_name = assistant_name
    def __call__(self, state: GraphState):
        messages = state[self.assistant_name+"_messages"]
        first_message = {"role":"system","content":self.prompt_text}
        
        
        # for message in messages:
        #     message.content
            
        #     if type(message) is tuple:
        #         print(message)
        #         (role,content) = message
        #         formatted_messages.append({"role":role,"content":content})

        messages = [first_message] + messages
        response = openai_client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            tools=self.tools_schema
        )
        message = response.choices[0].message

        tool_calls = message.tool_calls
        content = message.content
        message_obj = {"role":"assistant","content":content,"tool_calls":tool_calls}
        # print("-------------------XXXXXX")
        # print(message_obj)
        return {self.assistant_name+"_messages": [message_obj]}
    
class ProtoToolNode:
    """A node that runs the tools request ed in the last AIMessage."""

    def __init__(self, tools: list, assistant_name:str) -> None:
        self.tools_by_name = {tool.name: tool for tool in tools}
        self.assistant_name = assistant_name

    def __call__(self, state: GraphState):
        last_msg = state[self.assistant_name+"_messages"][-1]
        outputs = []
        for tool_call in last_msg["tool_calls"]:
            
            tool_result = self.tools_by_name[tool_call.function.name].invoke(
                json.loads(tool_call.function.arguments)
            )
           
            # outputs.append(
            #     ToolMessage(
            #         content=json.dumps(tool_result),
            #         name=tool_call.function.name,
            #         tool_call_id=id,
            #     )
            # )
            
            tool_call_id = tool_call.id
            tool_function_name = tool_call.function.name
            
            outputs.append(
                     {
                        "role":"tool", 
                        "tool_call_id":tool_call_id, 
                        "name": tool_function_name, 
                        "content":tool_result
                      }
              )
        return {self.assistant_name+"_messages": outputs}
    
tools_schema = [
    {
        "type": "function",
        "function": {
            "name": "parse_page",
            "description": "Parse and return text from any given url",
            "parameters": {
                "type": "object",
                "properties": {
                    "url": {
                        "type": "string",
                        "description": "URL of the website to parse",
                    },
                    
                },
                "required": ["url"],
            },
        }
    }]

prompt_text = "Your are a helpful online website parser assistant bot.Your primary role is to talk to user, ask them what url they want parsed. Once they give you the url, call the parser tool, and then get back to the user with the summary of the results."
assistant_one_tools = [BasicTool(parse_page,"parse_page")]
assistant_one_tools_node=ProtoToolNode(assistant_one_tools,"assistant_one")

workflow = StateGraph(GraphState)
assistant_one_node = OpenAIAssistant(prompt_text, tools_schema,"assistant_one")
workflow.add_node("assistant_one", assistant_one_node)
workflow.add_node("assistant_one_tools", assistant_one_tools_node)
workflow.add_edge("assistant_one_tools","assistant_one")
from functools import partial
workflow.add_conditional_edges("assistant_one",partial(tools_condition_edge,"assistant_one"),{"tools": "assistant_one_tools", "__end__": "__end__","assistant":"assistant_one"})

from user_info import user_info_node

workflow.add_node("user_info", user_info_node)
workflow.add_node("restream_message", restream_message)
workflow.add_edge("user_info","restream_message")
workflow.add_conditional_edges("restream_message", route_to_workflow)
workflow.set_entry_point("user_info")

memory = SqliteSaver.from_conn_string(":memory:")
graph = workflow.compile(checkpointer=memory)
import uuid

thread_id = str(uuid.uuid4())
config = {"configurable": {"thread_id": thread_id}}

if __name__ == "__main__":
    while True:
        user_msg = input("You: ")

        events = graph.stream({"last_user_message":user_msg},config)
        # this one here is interesting because if you have multiple ones, you'd need to re-stream the message into the proper one
        for event in events:
            print(event)


