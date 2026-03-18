import whisper
from pathlib import Path

model = None

def transcribe_audio(file_path: str) -> str:
    global model
    if model is None:
        model = whisper.load_model("base")
    
    result = model.transcribe(str(Path(file_path)), language="es")

    return result["text"].strip()

