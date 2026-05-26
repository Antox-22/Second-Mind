from app.core.models import Note
from app.core.normalize import normalize_text
from app.core.chunking import split_sentences, semantic_chunking_batch, batch_embedder
from test import notes

with open("text.txt", "w") as f:

    for note in notes.ALL_NOTES:

        chunks = semantic_chunking_batch(
            sentences=split_sentences(note),
            get_embeddings_batch_func=batch_embedder,
            note_id=1
        )

        f.write("\n".join([c.text for c in chunks]))
        f.write("\n\n---------\n\n")