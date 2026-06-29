import json
import os

from openai import AzureOpenAI

client = AzureOpenAI(
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version=os.getenv("AZURE_OPENAI_API_VERSION")
)

DEPLOYMENT = os.getenv("AZURE_OPENAI_DEPLOYMENT")

 
def analyze_call(transcript):

    prompt = f"""
You are a Quality Assurance Manager for an insurance company.

Analyze the complete conversation.

Return ONLY JSON.

{{
"summary":"",
"sentiment":"",
"customer_interest":"",
"call_outcome":"",
"follow_up_required":true,
"follow_up_reason":""
}}

Conversation

{transcript}
"""

    response = client.chat.completions.create(
        model=DEPLOYMENT,
        messages=[
            {
                "role":"user",
                "content":prompt
            }
        ],
        temperature=0
    )

    return json.loads(
        response.choices[0].message.content
    )