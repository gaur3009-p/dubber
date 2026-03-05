import gradio as gr
import uuid

from services.asr import transcribe_audio
from services.translate import translate_text
from services.tts import clone_voice, generate_speech


# Store voice id for session
current_voice_id = None


# -----------------------------
# Voice Cloning Function
# -----------------------------
def register_voice(audio_path):

    global current_voice_id

    if audio_path is None:
        return "Please record a voice sample first."

    try:
        voice_id = clone_voice(audio_path)

        current_voice_id = voice_id

        return f"Voice cloned successfully! Voice ID: {voice_id}"

    except Exception as e:
        return f"Voice cloning failed: {str(e)}"


# -----------------------------
# Translate + Speak Function
# -----------------------------
def translate_and_speak(audio_path, target_lang):

    global current_voice_id

    if current_voice_id is None:
        return "Clone your voice first.", "", None

    if audio_path is None:
        return "Please record speech.", "", None

    try:

        # Speech → Text
        original_text = transcribe_audio(audio_path)

        # Translate
        translated_text = translate_text(original_text, target_lang)

        # Generate speech
        audio_output = generate_speech(translated_text, current_voice_id)

        return original_text, translated_text, audio_output

    except Exception as e:
        return f"Error: {str(e)}", "", None


# -----------------------------
# Language Options
# -----------------------------
language_options = {
    "English": "eng_Latn",
    "Hindi": "hin_Deva",
    "French": "fra_Latn",
    "Spanish": "spa_Latn"
}


# -----------------------------
# Gradio UI
# -----------------------------
with gr.Blocks() as demo:

    gr.Markdown("# 🎙 Multilingual Voice Cloner (Phase 1)")
    gr.Markdown("Clone your voice → Speak → Hear translation in your voice")

    # -------- Voice Cloning Tab --------
    with gr.Tab("1️⃣ Clone Your Voice"):

        voice_sample = gr.Audio(
            type="filepath",
            label="Record 15 seconds of your voice"
        )

        clone_btn = gr.Button("Clone Voice")

        clone_output = gr.Textbox(label="Clone Status")

        clone_btn.click(
            fn=register_voice,
            inputs=voice_sample,
            outputs=clone_output
        )

    # -------- Translation Tab --------
    with gr.Tab("2️⃣ Translate & Speak"):

        speech_input = gr.Audio(
            type="filepath",
            label="Speak something"
        )

        lang_dropdown = gr.Dropdown(
            choices=list(language_options.keys()),
            label="Target Language"
        )

        translate_btn = gr.Button("Translate & Speak")

        original_box = gr.Textbox(label="Original Text")

        translated_box = gr.Textbox(label="Translated Text")

        audio_output = gr.Audio(label="Cloned Voice Output")

        translate_btn.click(
            fn=lambda a, l: translate_and_speak(a, language_options[l]),
            inputs=[speech_input, lang_dropdown],
            outputs=[original_box, translated_box, audio_output]
        )


# -----------------------------
# Launch App
# -----------------------------
demo.launch(share = True)
