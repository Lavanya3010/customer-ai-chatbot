import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY is missing from .env file")

client = genai.Client(api_key=api_key)


def ask_ai(question: str) -> str:
    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=question
    )

    return response.text or ""