import gradio as gr

from services.asr import transcribe_audio
from services.translate import translate_text
from services.tts import clone_voice, generate_speech


current_voice_id = None


def register_voice(audio_path):

    global current_voice_id

    print("Audio received:", audio_path)

    if audio_path is None:
        return "Please record a voice sample first."

    try:

        voice_id = clone_voice(audio_path)

        current_voice_id = voice_id

        return f"Voice cloned successfully! Voice ID: {voice_id}"

    except Exception as e:
        return f"Voice cloning failed: {str(e)}"


def translate_and_speak(audio_path, target_lang):

    global current_voice_id

    if current_voice_id is None:
        return "Clone voice first", "", None

    if audio_path is None:
        return "Please record speech", "", None

    try:

        original_text = transcribe_audio(audio_path)

        translated_text = translate_text(original_text, target_lang)

        audio_file = generate_speech(translated_text, current_voice_id)

        return original_text, translated_text, audio_file

    except Exception as e:
        return f"Error: {str(e)}", "", None


language_options = {
    "English": "eng_Latn",
    "Hindi": "hin_Deva",
    "French": "fra_Latn",
    "Spanish": "spa_Latn"
}


with gr.Blocks() as demo:

    gr.Markdown("# Multilingual Voice Translator")

    with gr.Tab("Clone Voice"):

        voice_sample = gr.Audio(
            sources=["microphone"],
            type="filepath",
            label="Record 10–15 seconds of your voice"
        )

        clone_btn = gr.Button("Clone Voice")

        clone_status = gr.Textbox(label="Clone Status")

        clone_btn.click(
            register_voice,
            inputs=voice_sample,
            outputs=clone_status
        )

    with gr.Tab("Translate & Speak"):

        speech_input = gr.Audio(
            sources=["microphone"],
            type="filepath",
            label="Speak something"
        )

        language = gr.Dropdown(
            list(language_options.keys()),
            label="Target Language"
        )

        translate_btn = gr.Button("Translate & Speak")

        original = gr.Textbox(label="Original Text")
        translated = gr.Textbox(label="Translated Text")

        output_audio = gr.Audio(label="Generated Speech")

        translate_btn.click(
            lambda a, l: translate_and_speak(a, language_options[l]),
            inputs=[speech_input, language],
            outputs=[original, translated, output_audio]
        )


demo.launch(share=True)
