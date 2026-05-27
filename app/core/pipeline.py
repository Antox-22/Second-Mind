from app.core.models import Note
from app.core.normalize import normalize_text
from app.core.emotion import get_emotion
from app.core.chunking import split_sentences, semantic_chunking_batch, batch_embedder
from test import notes
import json

with open("text.txt", "w") as f:

    # for note in notes.ALL_NOTES:

    chunks = semantic_chunking_batch(
        sentences=split_sentences(notes.NOTE_1),
        get_embeddings_batch_func=batch_embedder,
        note_id=1
    )

    for c in chunks:

        f.write(c.text)
        f.write("\n\n----------\n\n")
        f.write(json.dumps(get_emotion(c.text)))
        f.write("\n\n----->----\n\n")


    f.write("\n\n----EDN-----\n\n")