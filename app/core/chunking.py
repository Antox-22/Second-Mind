from app.core.load_model import nlp, embedding_model as model
from app.core.models import Chunk
import numpy as np


def split_sentences(text: str) -> list[str]:
    doc = nlp(text)
    return [sent.text.strip() for sent in doc.sents if sent.text.strip()]


def _normalize(vec) -> np.ndarray:
    arr = np.asarray(vec, dtype=np.float32)
    norm = np.linalg.norm(arr)
    if norm == 0:
        return arr
    return arr / norm


def batch_embedded(texts: list[str], prefix: str = "passage: ") -> list[list[float]]:
    texts = [f"{prefix}{t}" for t in texts]
    embeddings = model.encode(texts, normalize_embeddings=True)
    return embeddings.tolist()


def cosine_similarity(vec1, vec2) -> float:
    v1 = _normalize(vec1)
    v2 = _normalize(vec2)
    return float(np.dot(v1, v2))


def semantic_chunking_batch(
    sentences: list[str],
    note_id: int,
    threshold: float = 0.55,
    max_chars: int = 1000,
    lookback: int = 3,
    min_sentence_len_to_split: int = 25,
) -> list[Chunk]:

    if not sentences:
        return []

    sentences = [s.strip() for s in sentences if s and s.strip()]
    if not sentences:
        return []

    embeddings = np.asarray(batch_embedded(sentences), dtype=np.float32)

    chunks: list[Chunk] = []

    current_sentences = [sentences[0]]
    current_embeddings = [embeddings[0]]
    current_chars = len(sentences[0])
    prev_sentence_emb = embeddings[0]

    for i in range(1, len(sentences)):
        sentence = sentences[i]
        sentence_emb = embeddings[i]

        recent_embs = np.asarray(current_embeddings[-lookback:], dtype=np.float32)
        chunk_centroid = np.mean(recent_embs, axis=0)

        sim_to_chunk = cosine_similarity(chunk_centroid, sentence_emb)
        sim_to_prev = cosine_similarity(prev_sentence_emb, sentence_emb)

        projected_chars = current_chars + 1 + len(sentence)

        should_split = (
            projected_chars > max_chars
            or (
                len(current_sentences) >= 2
                and len(sentence) >= min_sentence_len_to_split
                and sim_to_chunk < threshold
                and sim_to_prev < threshold
            )
        )

        if should_split:
            chunk_text = " ".join(current_sentences).strip()
            chunk_embedding = _normalize(np.mean(current_embeddings, axis=0)).tolist()

            chunks.append(
                Chunk(
                    text=chunk_text,
                    sentences=current_sentences.copy(),
                    note_id=note_id,
                    embedding=chunk_embedding,
                )
            )

            current_sentences = [sentence]
            current_embeddings = [sentence_emb]
            current_chars = len(sentence)
        else:
            current_sentences.append(sentence)
            current_embeddings.append(sentence_emb)
            current_chars = projected_chars

        prev_sentence_emb = sentence_emb

    if current_sentences:
        chunk_text = " ".join(current_sentences).strip()
        chunk_embedding = _normalize(np.mean(current_embeddings, axis=0)).tolist()

        chunks.append(
            Chunk(
                text=chunk_text,
                sentences=current_sentences.copy(),
                note_id=note_id,
                embedding=chunk_embedding,
            )
        )

    return chunks