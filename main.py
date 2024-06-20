from fastapi import FastAPI, HTTPException

from models import UserMessagePayload
from langchain_core.messages import  HumanMessage
from services.bot_logic import graph
app = FastAPI()

@app.get("/")
def root():
    return {"message": "Hello World"}




@app.post("/messages")
def add_human_message(user_message_payload: UserMessagePayload):
    user_message = user_message_payload.content
    conversation_id = user_message_payload.conversation_id
    config = {"configurable": {"thread_id": conversation_id}}

    user_message = HumanMessage(
                content=user_message
            )
    events = graph.stream({"messages":[user_message]},config)
    for event in events:
        print(event)
    ai_message = event.messages[-1].content
       
    return {"ai_message": ai_message}