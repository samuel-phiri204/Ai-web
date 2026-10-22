import time
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
app = Flask(__name__)
CORS(app)
client = genai.Client()  # reads GEMINI_API_KEY from .env

MODELS = ["gemini-flash-latest", "gemini-2.5-flash", "gemini-2.5-flash-lite"]

def generate(text):
    last_error = None
    for model in MODELS:
        for attempt in range(2):
            try:
                response = client.models.generate_content(
                    model=model,
                    contents=text,
                    config=types.GenerateContentConfig(
                        system_instruction="You are a study helper for university students. Explain or answer the highlighted text clearly and briefly.",
                        max_output_tokens=600,
                    ),
                )
                return response.text
            except Exception as e:
                last_error = e
                print(model, e)
                time.sleep(1)
    raise last_error

@app.post("/ask")
def ask():
    text = (request.get_json() or {}).get("text", "").strip()[:2000]
    if not text:
        return jsonify(error="No text selected"), 400
    try:
        return jsonify(answer=generate(text))
    except Exception:
        return jsonify(error="The AI is busy right now. Please try again in a minute."), 503

if __name__ == "__main__":
    app.run(port=5000)