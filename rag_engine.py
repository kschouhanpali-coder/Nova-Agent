import os
import math
import string
import streamlit as st
from typing import List, Dict

from config import AGENT_MAPPING


class TFIDFRetriever:
    """TF-IDF based document retriever for RAG."""
    
    def __init__(self, chunks: List[Dict[str, str]]):
        self.chunks = chunks
        self.stopwords = {"the", "a", "an", "and", "or", "but", "is", "are", "was", "were", "to", "of", "in", "on", "at", "for", "with"}
        self.idf = {}
        self.doc_tfs = []
        self._build_index()
        
    def _tokenize(self, text: str) -> List[str]:
        text = text.lower().translate(str.maketrans('', '', string.punctuation))
        return [t for t in text.split() if t not in self.stopwords]
        
    def _build_index(self):
        N = len(self.chunks)
        if N == 0: return
        df = {}
        for chunk in self.chunks:
            tokens = self._tokenize(chunk["content"])
            tf = {}
            for token in tokens: tf[token] = tf.get(token, 0) + 1
            self.doc_tfs.append(tf)
            for token in set(tokens): df[token] = df.get(token, 0) + 1
        for token, count in df.items():
            self.idf[token] = math.log(1 + (N / (1 + count)))
            
    def retrieve(self, query: str, top_k: int = 5) -> List[tuple]:
        query_tokens = self._tokenize(query)
        if not query_tokens or not self.chunks: return [(chunk, 0.0) for chunk in self.chunks[:top_k]]
        
        query_tf = {}
        for t in query_tokens: query_tf[t] = query_tf.get(t, 0) + 1
        
        query_tfidf = {t: c * self.idf.get(t, 0) for t, c in query_tf.items() if t in self.idf}
        query_len = math.sqrt(sum(v*v for v in query_tfidf.values()))
        
        if query_len == 0: return [(chunk, 0.0) for chunk in self.chunks[:top_k]]
        
        scores = []
        for i, doc_tf in enumerate(self.doc_tfs):
            dot_product = sum(query_tfidf[t] * (tf * self.idf.get(t, 0)) for t, tf in doc_tf.items() if t in query_tfidf)
            doc_len = math.sqrt(sum((tf * self.idf.get(t, 0))**2 for t, tf in doc_tf.items()))
            sim = dot_product / (query_len * doc_len) if doc_len > 0 else 0.0
            scores.append((self.chunks[i], sim))
            
        scores.sort(key=lambda x: x[1], reverse=True)
        return scores[:top_k]


def chunk_document(content: str) -> List[Dict[str, str]]:
    """Split a markdown document into chunks by ## headers."""
    chunks, current_header, current_lines = [], "Intro", []
    for line in content.split("\n"):
        if line.startswith("## "):
            if current_lines: chunks.append({"header": current_header, "content": "\n".join(current_lines).strip()})
            current_header, current_lines = line.replace("##", "").strip(), []
        else: current_lines.append(line)
    if current_lines: chunks.append({"header": current_header, "content": "\n".join(current_lines).strip()})
    return [c for c in chunks if len(c["content"].split()) > 15]


@st.cache_resource
def load_rag_indices():
    """Load and index all RAG documents for each agent."""
    retrievers = {}
    for a_id, info in AGENT_MAPPING.items():
        paths = [f"backend/data/rag_documents/{info['rag_file']}", f"backend/{info['rag_file']}", info['rag_file']]
        file_path = next((p for p in paths if os.path.exists(p)), None)
        if file_path:
            with open(file_path, "r", encoding="utf-8") as f:
                retrievers[a_id] = TFIDFRetriever(chunk_document(f.read()))
        else: retrievers[a_id] = None
    return retrievers
