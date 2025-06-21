from typing import Final
from dataclasses import dataclass
from pathlib import Path

@dataclass(frozen=True)
class Config:
    EMBEDDING_MODEL: Final[str] = "sentence-transformers/all-MiniLM-L6-v2"
    CHUNK_SIZE: Final[int] = 500
    CHUNK_OVERLAP: Final[int] = 50
    VECTOR_STORE_PATH: Final[str] = "data/processed/index.faiss"
    EMBEDDINGS_PATH: Final[str] = "data/processed/embeddings.pkl"

    def __post_init__(self):
        if self.CHUNK_OVERLAP >= self.CHUNK_SIZE:
            raise ValueError("CHUNK_OVERLAP must be less than CHUNK_SIZE")
        
        if self.CHUNK_SIZE <= 0 or self.CHUNK_OVERLAP < 0:
            raise ValueError("CHUNK_SIZE and CHUNK_OVERLAP must be positive")
        
        # Ensure directories exist
        for path in [self.VECTOR_STORE_PATH, self.EMBEDDINGS_PATH]:
            Path(path).parent.mkdir(parents=True, exist_ok=True)

config = Config()
