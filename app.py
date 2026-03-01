import gradio as gr
import uuid
import shutil
from services.asr import transcribe_audio
from services.translate import translate_text
from services.tts import clone_voice, generate_speech

current_voice_id = None

def register_voice(audio_file):

    global current_voice_id

    temp_filename = f"voice_{uuid.uuid4()}.wav"
    shutil.copy(audio_file, temp_filename)

    voice_id = clone_voice(temp_filename)
    current_voice_id = voice_id

    return f"Voice cloned successfully! Voice ID: {voice_id}"


def translate_and_speak(audio_file, target_lang):

    global current_voice_id

    if current_voice_id is None:
        return "Please clone voice first", "", None

    temp_filename = f"temp_{uuid.uuid4()}.wav"
    shutil.copy(audio_file, temp_filename)

    original_text = transcribe_audio(temp_filename)
    translated_text = translate_text(original_text, target_lang)

    output_audio = generate_speech(translated_text, current_voice_id)

    return original_text, translated_text, output_audio


language_options = {
    "English": "eng_Latn",
    "Hindi": "hin_Deva",
    "French": "fra_Latn",
    "Spanish": "spa_Latn"
}

with gr.Blocks() as demo:

    gr.Markdown("## Phase 1 – Multilingual Voice Cloner")

    with gr.Tab("1️⃣ Clone Your Voice"):
        voice_sample = gr.Audio(type="filepath", label="Record 15 seconds of clear speech")
        clone_btn = gr.Button("Clone Voice")
        clone_output = gr.Textbox(label="Clone Status")

        clone_btn.click(
            fn=register_voice,
            inputs=voice_sample,
            outputs=clone_output
        )

    with gr.Tab("2️⃣ Translate & Speak"):
        speech_input = gr.Audio(type="filepath", label="Speak something")
        lang_dropdown = gr.Dropdown(choices=list(language_options.keys()), label="Target Language")
        translate_btn = gr.Button("Translate & Speak")

        original_box = gr.Textbox(label="Original Text")
        translated_box = gr.Textbox(label="Translated Text")
        audio_output = gr.Audio(label="Cloned Voice Output")

        translate_btn.click(
            fn=lambda a, l: translate_and_speak(a, language_options[l]),
            inputs=[speech_input, lang_dropdown],
            outputs=[original_box, translated_box, audio_output]
        )

demo.launch()
