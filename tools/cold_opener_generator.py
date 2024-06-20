from openai import OpenAI
from langchain_core.tools import tool

@tool
def generate_cold_opener(company_description:str):
    """
    Generate answer

    Args:
        company_description (str): The description of the company we are targeting

    Returns:
         col_opener (str): text that can be inserted into an email
    """
   
    context = company_description
    prompt_text = f"You are an expert at writing cold emails. Draft a perfect cold email for the company whose descrpition is provided in the context: <<<context: {context}>>> Your answer should be 2 sentence long, and should give a compliment relevant to the context"

    messages = [{"role":"system","content":prompt_text}]
    client = OpenAI(api_key="sk-asdf-MkRgagrNycwmFmr1GjjgT3BlbkFJfKklQh0NsVMxUMkf9S8B")
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
    )
    result = response.choices[0].message.content
    return result