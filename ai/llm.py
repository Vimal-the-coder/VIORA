from google import genai
from config import Config


if not Config.LLM_API_KEY:
    raise ValueError("LLM_API_KEY is missing from .env")


client = genai.Client(api_key=Config.LLM_API_KEY)


def ask_ai(prompt, context=None):

    if context:
        full_prompt = f"""
You are VIORA, a helpful Windows voice assistant.

Previous conversation:
{context}

Current user message:
{prompt}

Answer naturally and concisely.
"""
    else:
        full_prompt = f"""
You are VIORA, a helpful Windows voice assistant.

Current user message:
{prompt}

Answer naturally and concisely.
"""

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=full_prompt
    )

    return response.text