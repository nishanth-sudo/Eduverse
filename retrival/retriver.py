from embeddings.vector_score import load_index
from sentence_transformers import SentenceTransformer
from config import EMBEDDING_MODEL
import re


model = SentenceTransformer(EMBEDDING_MODEL)

def retrieve_passages(query, top_k=5, include_images=True):
    
    index, passages = load_index()
    query_vec = model.encode([query])[0].reshape(1, -1)
    D, I = index.search(query_vec, top_k)
    
    # Optional: Filter/Boost passages with code or image keywords
    preferred_passages = []
    for i in I[0]:
        passage = passages[i]
        passage_lower = passage.lower()
        
        # Check if passage contains code references
        contains_code = any(kw in passage_lower for kw in ["example", "code", "import", "def", "class", "for ", "print"])
        
        # Prioritize based on query and content
        if contains_code:
            preferred_passages.insert(0, passage)  # Prioritize code-related
        else:
            preferred_passages.append(passage)
    
    return preferred_passages[:top_k]
