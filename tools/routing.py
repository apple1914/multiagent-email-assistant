from langchain_core.tools import tool

@tool
def route_to_main_assistant():
    """
    Transfers work back to the main assistant

    Returns:
        state: new state
    """
    
    return {"accept_suggested_company":False}   
