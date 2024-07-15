from src import _static
import copy
import os
from openai import AzureOpenAI

client = AzureOpenAI(
    azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT"), 
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),  
    api_version="2023-05-15"
)


def api_post_llm(
        l_context: list[str],
        messages: list[dict],
        select_model: str
    )-> list[dict]:
    # retrive the context for the top k
    retrieved_context = '\n'.join(l_context)
    # Add the retrieved context to the last message from the user
    messages_copy = copy.deepcopy(messages)
    messages_copy[-1]["content"] += f"\n Context: {retrieved_context}"
    messages_copy.insert(0,
        {
            "role": "system",
            "content": _static.INIT_CONTENT
        }
    )
    response = client.chat.completions.create(
        model=select_model,
        messages=messages_copy,
        temperature=_static.TEMPERATURE
    )
    return response.choices[0].message.content


def create_embedding(prompt: str)-> list:
    response = client.embeddings.create(
        input = [prompt],
        model = _static.EMBEDDING_MODEL
    )
    return response.data[0].embedding