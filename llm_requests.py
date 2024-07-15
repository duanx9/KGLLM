import pandas as pd
import requests
import os
from openai import AzureOpenAI

client = AzureOpenAI(
    azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT"), 
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),  
    api_version="2023-05-15"
)

def concat_context_message(prompt_init: str, query: str, context: str)-> str:
    context_joined = '\n'.join(context)
    full_content = f"""
        {prompt_init}
        User: {query}
        Context: {context_joined}
    """
    return full_content

def api_post_llm(
        full_content: str
    )-> list[dict]:

    response = client.chat.completions.create(
        model="xxx", # GPT-3.5-Turbo or GPT-4
        messages=[
            {
                "role": "user", 
                "content": full_content
            }
        ]
    )
    print(response.choices[0].message.content)
    
    return response.choices[0].message.content