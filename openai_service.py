from openai import AzureOpenAI
from config import (
    AZURE_OPENAI_ENDPOINT,
    AZURE_OPENAI_KEY,
    AZURE_OPENAI_DEPLOYMENT,
    AZURE_OPENAI_API_VERSION,
)

client = AzureOpenAI(
    azure_endpoint=AZURE_OPENAI_ENDPOINT,
    api_key=AZURE_OPENAI_KEY,
    api_version=AZURE_OPENAI_API_VERSION,
)

SYSTEM_PROMPT = """
You are an AI Voice Assistant for Tata Insurance.

Customer Name: Nikhil Patil
Policy Number: Tata123

Your responsibilities:
1. Greet the customer.
2. Verify the policy number.
3. Answer questions naturally.
4. Recommend insurance plans if asked.
5. End the conversation politely.
Keep responses short and conversational.
"""

def get_ai_response(messages):
    response = client.chat.completions.create(
        model=AZURE_OPENAI_DEPLOYMENT,
        messages=messages,
        temperature=0.4,
        max_tokens=150,
    )

    return response.choices[0].message.content