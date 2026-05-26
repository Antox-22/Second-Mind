from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime, timezone
from itertools import count

_id_note_counter = count(1)
_id_chunk_counter = count(1)

@dataclass
class Chunk:
    note_id: int
    text: str
    id: int = field(default_factory=lambda: next(_id_chunk_counter))
    embedding: Optional[List[float]] = None
    emotion: Optional[str] = None
    emotion_confidence: Optional[float] = None
    create_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

@dataclass
class Note:
    raw_text: str
    id: int = field(default_factory=lambda: next(_id_note_counter))
    chunks: List[Chunk] = field(default_factory=list)
    create_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))