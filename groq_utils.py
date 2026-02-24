import os
from groq import Groq
import json

def get_groq_client():
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY not set in environment variables.")
    return Groq(api_key=api_key)


def call_groq(system_prompt, user_prompt):
    client = get_groq_client()

    response = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.3,
    )

    return response.choices[0].message.content


def safe_json_loads(text):
    try:
        return json.loads(text)
    except:
        return None