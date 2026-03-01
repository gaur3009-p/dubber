import requests
import os
from dotenv import load_dotenv
import uuid

load_dotenv()

API_KEY = os.getenv("ELEVEN_API_KEY")
VOICE_ID = os.getenv("VOICE_ID")

def generate_speech(text):
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"

    headers = {
        "xi-api-key": API_KEY,
        "Content-Type": "application/json"
    }

    payload = {
        "text": text,
        "model_id": "eleven_multilingual_v2"
    }

    response = requests.post(url, json=payload, headers=headers)

    filename = f"output_{uuid.uuid4()}.mp3"

    with open(filename, "wb") as f:
        f.write(response.content)

    return filename
