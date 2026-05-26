from app.core.models import Note
from app.core.normalize import normalize_text
from app.core.chunking import split_sentences, build_chunks
from test import notes

note = Note(
    raw_text=normalize_text(notes.NOTE_1)
)

print(build_chunks(split_sentences(note.raw_text)))