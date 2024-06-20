
from graph_state import GraphState
from typing import Literal,Callable
from langchain_core.runnables import Runnable
from langgraph.graph import END, StateGraph
from langgraph.prebuilt import ToolNode
from langgraph.checkpoint.sqlite import SqliteSaver
from tools.company_retriever import company_retriever_tool
from langchain.prompts import ChatPromptTemplate
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import AIMessage, HumanMessage
from tools.routing import route_to_main_assistant
from edges.contionoal_edges import from_main_assistant_edge, from_evaluator_assistant_edge, from_evaluator_assistant_tools_edge, route_to_workflow
from tools.cold_opener_generator import generate_cold_opener

llm = ChatAnthropic(model="claude-3-haiku-20240307")


def create_entry_node(assistant_name: str) -> Callable:
    def entry_node(state: GraphState) -> dict:
        return {
            "dialogue_state": assistant_name,
        }

    return entry_node
    
class Assistant:
    def __init__(self, runnable: Runnable):
        self.runnable = runnable

    def __call__(self, state: GraphState):
        result = self.runnable.invoke(state)
        return {"messages": [result]}


main_assistant_tools = [company_retriever_tool]
main_assistant_tools_node=ToolNode(main_assistant_tools)
main_assitant_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "Your are a helpful research assistant bot. "
            "Your primary role is to talk to user, and help them form a query to ask. Once the query is ready, call the retriever tool with the query "
            ,
        ),
        ("placeholder", "{messages}"),
    ]
)
main_assitant_runnable = main_assitant_prompt | llm.bind_tools(main_assistant_tools)
main_assistant_entry_node = create_entry_node("main_assistant")




    
 

evaluator_assistant_tools = [route_to_main_assistant,generate_cold_opener]
evaluator_assistant_tools_node=ToolNode(evaluator_assistant_tools)
evaluator_assitant_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "Your are a helpful research assistant bot. "
            "Your primary goal is to talk to the user and see if they are happy with the suggestted examplse. If they are not happy, call the route to main assistant tool to try againIf they are, call generate_cold_opener tool to generate the cold opener with the descirption of the company. Then report back to the user with the result of the generate_cold_opener tool."
            ,
        ),
        ("placeholder", "{messages}"),
    ]
)
evaluator_assitant_runnable = evaluator_assitant_prompt | llm.bind_tools(evaluator_assistant_tools)
evaluator_assistant_entry_node = create_entry_node("evaluator_assistant")


    
    
workflow = StateGraph(GraphState)
workflow.add_node("main_assistant_entry_node", main_assistant_entry_node)
workflow.add_node("main_assistant", Assistant(main_assitant_runnable))
workflow.add_node("main_assistant_tools_node", main_assistant_tools_node)
workflow.add_edge("main_assistant_entry_node","main_assistant")

workflow.add_conditional_edges("main_assistant",from_main_assistant_edge)
workflow.add_node("evaluator_assistant_entry_node", evaluator_assistant_entry_node)
workflow.add_node("evaluator_assistant", Assistant(evaluator_assitant_runnable))
workflow.add_node("evaluator_assistant_tools_node", evaluator_assistant_tools_node)


workflow.add_edge("main_assistant_tools_node","evaluator_assistant_entry_node")
workflow.add_edge("evaluator_assistant_entry_node","evaluator_assistant")
workflow.add_conditional_edges("evaluator_assistant",from_evaluator_assistant_edge)
workflow.add_conditional_edges("evaluator_assistant_tools_node",from_evaluator_assistant_tools_edge)






from tools.user_info import user_info_node



    
workflow.add_node("user_info", user_info_node)
workflow.set_entry_point("user_info")
workflow.add_conditional_edges("user_info", route_to_workflow)
memory = SqliteSaver.from_conn_string(":memory:")
graph = workflow.compile(checkpointer=memory)

