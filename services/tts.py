from elevenlabs.client import ElevenLabs
import os
import uuid


def get_client():
    api_key = os.getenv("ELEVEN_API_KEY")

    if not api_key:
        raise Exception("ELEVEN_API_KEY environment variable not set")

    return ElevenLabs(api_key=api_key)


def clone_voice(audio_path):

    client = get_client()

    if not os.path.exists(audio_path):
        raise Exception(f"Audio file not found: {audio_path}")

    with open(audio_path, "rb") as audio_file:

        voice = client.voices.create(
            name=f"user_voice_{uuid.uuid4()}",
            files=[audio_file]
        )

    return voice.voice_id


def generate_speech(text, voice_id):

    client = get_client()

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
