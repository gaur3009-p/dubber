import requests
import os
import uuid
from elevenlabs.client import ElevenLabs


def get_api_key():
    api_key = os.getenv("ELEVEN_API_KEY")

    if not api_key:
        raise Exception("ELEVEN_API_KEY environment variable not set")

    return api_key


# ----------------------------
# Voice Cloning (REST API)
# ----------------------------
def clone_voice(audio_path):

    api_key = get_api_key()

    url = "https://api.elevenlabs.io/v1/voices/add"

    headers = {
        "xi-api-key": api_key
    }

    files = [
        ("files", (audio_path, open(audio_path, "rb"), "audio/wav"))
    ]

    data = {
        "name": f"user_voice_{uuid.uuid4()}"
    }

    response = requests.post(
        url,
        headers=headers,
        files=files,
        data=data
    )

    if response.status_code != 200:
        raise Exception(f"Voice cloning failed: {response.text}")

    result = response.json()

    return result["voice_id"]


# ----------------------------
# Speech Generation (SDK)
# ----------------------------
def generate_speech(text, voice_id):

    api_key = get_api_key()

    client = ElevenLabs(api_key=api_key)

    audio = client.text_to_speech.convert(
        text=text,
        voice_id=voice_id,
        model_id="eleven_multilingual_v2",
        output_format="mp3_44100_128"
    )

    output_file = f"output_{uuid.uuid4()}.mp3"

    with open(output_file, "wb") as f:
        f.write(audio)

    return output_file
