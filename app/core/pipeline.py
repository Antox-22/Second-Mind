from app.core.models import Note
from app.core.normalize import normalize_text
from app.core.chunking import split_sentences, semantic_chunking_batch, batch_embedder
from test import notes
import json

with open("test.json", "w") as f:
    json.dump(
        semantic_chunking_batch(
            sentences=split_sentences(notes.NOTE_1),
            get_embeddings_batch_func=batch_embedder
        ), f, indent=2
    )