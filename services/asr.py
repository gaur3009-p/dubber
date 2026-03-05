from faster_whisper import WhisperModel
import torch

device = "cuda" if torch.cuda.is_available() else "cpu"

compute = "float16" if device == "cuda" else "int8"

model = WhisperModel(
    "base",
    device=device,
    compute_type=compute
)


def transcribe_audio(audio_path):

    segments, _ = model.transcribe(audio_path)

    text = ""

    for segment in segments:
        text += segment.text + " "

    return text.strip()
