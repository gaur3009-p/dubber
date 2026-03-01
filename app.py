import gradio as gr
import os
import uuid
import shutil
from dotenv import load_dotenv
from services.asr import transcribe_audio
from services.translate import translate_text
from services.tts import generate_speech

load_dotenv()

def process_audio(audio_file, target_lang):

    temp_filename = f"temp_{uuid.uuid4()}.wav"

    shutil.copy(audio_file, temp_filename)

    # 1️⃣ Speech → Text
    original_text = transcribe_audio(temp_filename)

    # 2️⃣ Translate
    translated_text = translate_text(original_text, target_lang)

    # 3️⃣ Generate Speech
    output_audio = generate_speech(translated_text)

    return original_text, translated_text, output_audio


language_options = {
    "English": "eng_Latn",
    "Hindi": "hin_Deva",
    "French": "fra_Latn",
    "Spanish": "spa_Latn"
}

demo = gr.Interface(
    fn=process_audio,
    inputs=[
        gr.Audio(type="filepath", label="Upload Speech"),
        gr.Dropdown(choices=list(language_options.keys()), label="Target Language")
    ],
    outputs=[
        gr.Textbox(label="Original Text"),
        gr.Textbox(label="Translated Text"),
        gr.Audio(label="Cloned Voice Output")
    ],
    title="Multilingual Voice Translator (Phase 1)",
    description="Upload speech → Translate → Hear it in your cloned voice"
)

demo.launch()
