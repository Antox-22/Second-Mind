from app.core.models import Note
from app.core.normalize import normalize_text
from app.core.emotion import set_chunks_emotion
from app.core.chunking import split_sentences, semantic_chunking_batch
from test import notes
import json


def create_note(
        title: str,
        text: str
    ) -> Note:

    _text = normalize_text(text)
    _title = normalize_text(title)

    _note = Note(
        raw_text=_text,
        title=_title
    )

    _chunks = semantic_chunking_batch(
        sentences=split_sentences(_text),
        note_id=_note.id
    )

    set_chunks_emotion(_chunks)

    _note.chunks = _chunks

    return _note

with open("text.txt","w", encoding="utf-8") as f:
    for c in create_note("a", notes.NOTE_1).chunks:
        f.write(c.text)
        f.write("\n\n--------------\n\n")