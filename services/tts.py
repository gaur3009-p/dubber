import requests
import os
import uuid
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("ELEVEN_API_KEY")

def clone_voice(audio_path, voice_name="UserVoice"):

    url = "https://api.elevenlabs.io/v1/voices/add"

    headers = {
        "xi-api-key": API_KEY
    }

    files = [
        ("files", (audio_path, open(audio_path, "rb"), "audio/wav"))
    ]

    data = {
        "name": f"{voice_name}_{uuid.uuid4()}"
    }

    response = requests.post(url, headers=headers, files=files, data=data)

    if response.status_code != 200:
        raise Exception(f"API Error {response.status_code}: {response.text}")

    response_data = response.json()

    if "voice_id" not in response_data:
        raise Exception(f"Voice cloning failed: {response_data}")

    return response_data["voice_id"]

def generate_speech(text, voice_id):

    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"

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
