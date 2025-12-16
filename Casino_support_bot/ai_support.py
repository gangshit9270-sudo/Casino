import os
import json
from google import genai
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise RuntimeError("❌ GEMINI_API_KEY не найден в .env")

client = genai.Client(api_key=GEMINI_API_KEY)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def ai_answer_support(prompt: str, message_file: str | None = None) -> dict:
    try:
        if message_file is None:
            message_file = os.path.join(BASE_DIR, "ai_settings.json")

        with open(message_file, "r", encoding="utf-8") as f:
            ai_settings = json.load(f)

        model = ai_settings["model"]
        system_prompt = ai_settings["system_instruction"]

        contents = [
            {
                "role": "user",
                "parts": [{"text": system_prompt}]
            },
            {
                "role": "user",
                "parts": [{"text": prompt}]
            }
        ]

        response = client.models.generate_content(
            model=model,
            contents=contents
        )

        return {"answer": response.text}

    except Exception as e:
        return {"error": str(e)}
