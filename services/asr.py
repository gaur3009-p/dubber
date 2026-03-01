from faster_whisper import WhisperModel

# Choose model size:
# tiny, base, small, medium, large-v3
model_size = "base"

model = WhisperModel(
    model_size,
    device="cuda",  # change to "cpu" if no GPU
    compute_type="float16"  # use "int8" for CPU
)

def transcribe_audio(file_path):
    segments, info = model.transcribe(file_path)

    full_text = ""
    for segment in segments:
        full_text += segment.text + " "

    return full_text.strip()
