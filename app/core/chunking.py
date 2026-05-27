from app.core.load_model import nlp, embedding_model as model
from app.core.models import Chunk
from app.core.emotion import get_emotion
import numpy as np


def split_sentences(text: str) -> list[str]:
    doc = nlp(text)
    return [sent.text for sent in doc.sents]

import numpy as np

def calculate_cosine_similarity(vec1: list[float], vec2: list[float]) -> float:
    v1 = np.array(vec1)
    v2 = np.array(vec2)
    return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))

def semantic_chunking_batch(
    sentences: list[str],
    get_embeddings_batch_func,
    note_id: int,
    threshold: float = 0.50,
    max_chars: int = 1000
) -> list[Chunk]:

    if not sentences:
        return []

    embeddings = get_embeddings_batch_func(sentences)

    chunks = []
    current_chunk = [sentences[0]]
    current_chunk_embeddings = [embeddings[0]] 
    current_length = len(sentences[0])

    for i in range(1, len(sentences)):
        sentence = sentences[i]
        sentence_emb = embeddings[i]

        recent_embeddings = current_chunk_embeddings[-3:]
        chunk_centroid = np.mean(recent_embeddings, axis=0)

        sim = calculate_cosine_similarity(chunk_centroid, sentence_emb)

        if (sim < threshold and len(sentence) >= 30) or (current_length + len(sentence) > max_chars):
            chunks.append(
                Chunk(
                    text=" ".join(current_chunk).strip(),
                    sentences=current_chunk,
                    note_id=note_id,
                    embedding=batch_embedder([" ".join(current_chunk).strip(),])[0]
                )
            )
            current_chunk = [sentence]
            current_chunk_embeddings = [sentence_emb]
            current_length = len(sentence)
        else:
            current_chunk.append(sentence)
            current_chunk_embeddings.append(sentence_emb)
            current_length += len(sentence)

    if current_chunk:
        chunks.append(
            Chunk(
                text=" ".join(current_chunk).strip(),
                sentences=current_chunk,
                note_id=note_id,
                embedding=batch_embedder([" ".join(current_chunk).strip(),])[0]
            )
        )

    return chunks

def batch_embedder(texts: list[str]):
    vec = model.encode(texts)
    return vec.tolist()