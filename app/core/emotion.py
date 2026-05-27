from app.core.models import Chunk
from app.core.load_model import emotion_model

def get_emotion(text: str) -> dict:
    text = text[:1500]

    result = emotion_model(text)
    return {
        "emotion": result[0]["label"],
        "score": round(result[0]["score"] * 100, 2)
    }

def set_chunks_emotion(chunks: list[Chunk]):
    for c in chunks:
        _result = get_emotion(c.text)

        c.emotion = _result["emotion"]
        c.emotion_confidence = _result["score"]