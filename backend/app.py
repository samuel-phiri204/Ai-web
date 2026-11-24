import time
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
app = Flask(__name__, static_folder="public", static_url_path="")
CORS(app)
client = genai.Client(http_options=types.HttpOptions(timeout=15000))  # reads GEMINI_API_KEY from .env

MODELS = ["gemini-3.5-flash", "gemini-3.5-flash-lite", "gemini-flash-lite-latest", "gemini-3.1-flash-lite"]

def generate(text):
    last_error = None
    for model in MODELS:
        try:
            response = client.models.generate_content(
                model=model,
                contents=text,
                config=types.GenerateContentConfig(
                    system_instruction=(
    "You are an exam coach for university students. "
    "Answer the highlighted text the way a strong student would in a written exam. "
    "Start with a clear definition or direct answer in one or two sentences. "
    "Then give the key points as short numbered points, using the correct technical terms. "
    "Add a brief example or diagram description where it helps. "
    "If the question would normally carry marks, say roughly how many points a full answer needs. "
    "Keep it focused and avoid long introductions."
),
                    max_output_tokens=1000,
                ),
            )
            return response.text
        except Exception as e:
            last_error = e
            print(model, e)
            time.sleep(1)
    raise last_error

@app.get("/")
def home():
    return app.send_static_file("study.html")

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