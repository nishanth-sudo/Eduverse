'''
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
'''

from embeddings.vector_score import load_index
from sentence_transformers import SentenceTransformer
from config import config
import requests
from bs4 import BeautifulSoup
import random
import time
import re
from typing import List

# Initialize the embedding model
EMBEDDING_MODEL = config.EMBEDDING_MODEL
model = SentenceTransformer(EMBEDDING_MODEL)

# User agent for web scraping
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36'
}

def retrieve_from_embeddings(query: str, top_k: int = 5) -> List[str]:
    """Retrieve passages from embeddings."""
    try:
        index, passages = load_index()
        query_vec = model.encode([query])[0].reshape(1, -1)
        D, I = index.search(query_vec, top_k)

        retrieved_passages = [passages[i] for i in I[0]]
        return retrieved_passages
    except Exception as e:
        print(f"Error retrieving from embeddings: {e}")
        return []

def retrieve_from_web(query: str) -> List[str]:
    """Retrieve passages from web articles."""
    try:
        # Example: GeeksForGeeks and W3Schools
        def search_geeksforgeeks(query: str) -> List[str]:
            search_query = "+".join(query.split())
            url = f"https://www.geeksforgeeks.org/search/?q={search_query}"
            response = requests.get(url, headers=HEADERS)
            if response.status_code != 200:
                return []
            soup = BeautifulSoup(response.text, 'html.parser')
            article_links = soup.select('article.content-card h2 a')[:2]
            passages = []
            for link in article_links:
                article_url = link['href']
                if not article_url.startswith('http'):
                    article_url = f"https://www.geeksforgeeks.org{article_url}"
                article_response = requests.get(article_url, headers=HEADERS)
                if article_response.status_code == 200:
                    article_soup = BeautifulSoup(article_response.text, 'html.parser')
                    article_content = article_soup.select_one('.article-body')
                    if article_content:
                        text = article_content.get_text(separator='\n')
                        text = re.sub(r'\n+', '\n', text)
                        text = re.sub(r'\s+', ' ', text)
                        passages.append(f"From GeeksForGeeks ({article_url}):\n{text[:1500]}...")
            return passages

        def search_w3schools(query: str) -> List[str]:
            search_query = "+".join(query.split())
            url = f"https://www.w3schools.com/search/search.php?q={search_query}"
            response = requests.get(url, headers=HEADERS)
            if response.status_code != 200:
                return []
            soup = BeautifulSoup(response.text, 'html.parser')
            tutorial_links = soup.select('.gs-title a.gs-title')[:2]
            passages = []
            for link in tutorial_links:
                tutorial_url = link['href']
                if not tutorial_url.startswith('http'):
                    tutorial_url = f"https://www.w3schools.com{tutorial_url}"
                tutorial_response = requests.get(tutorial_url, headers=HEADERS)
                if tutorial_response.status_code == 200:
                    tutorial_soup = BeautifulSoup(tutorial_response.text, 'html.parser')
                    tutorial_content = tutorial_soup.select_one('#main')
                    if tutorial_content:
                        text = tutorial_content.get_text(separator='\n')
                        text = re.sub(r'\n+', '\n', text)
                        text = re.sub(r'\s+', ' ', text)
                        passages.append(f"From W3Schools ({tutorial_url}):\n{text[:1500]}...")
            return passages

        # Combine results from multiple sources
        web_passages = []
        web_passages.extend(search_geeksforgeeks(query))
        web_passages.extend(search_w3schools(query))
        return web_passages
    except Exception as e:
        print(f"Error retrieving from web: {e}")
        return []

def retrieve_passages(query: str, top_k: int = 5) -> List[str]:
    """Retrieve relevant passages from embeddings and web articles."""
    try:
        # Retrieve from embeddings
        embedding_passages = retrieve_from_embeddings(query, top_k)
        print(f"Retrieved {len(embedding_passages)} passages from embeddings.")

        # Retrieve from web articles
        web_passages = retrieve_from_web(query)
        print(f"Retrieved {len(web_passages)} passages from web articles.")

        # Combine results
        combined_passages = embedding_passages + web_passages
        return combined_passages[:top_k]  # Limit to top_k results
    except Exception as e:
        print(f"Error in retrieve_passages: {e}")
        return []