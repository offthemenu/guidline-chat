import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

'''
The retrieval module is responsible for retrieving the most relevant chunks of text from the documents.
'''

DEVICE = "cpu"
EMBEDDING_MDOEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
embedder = SentenceTransformer(EMBEDDING_MDOEL_NAME, device = DEVICE)

def create_document_chunks(doc_texts, chunk_size=200):
    '''
    Turn the text into smaller chunks/tokens for retrieval purposes
    '''
    chunks = []
    for text in doc_texts:
        words = text.split()
        for i in range(0, len(words), chunk_size):
            chunk = " ".join(words[i:i+chunk_size])
            chunks.append(chunk)
    return chunks # Return the chunks

def build_faiss_index(chunks):
    '''
    Builds a FAISS index for the chunks
    '''
    chunk_embeddings = embedder.encode(chunks, convert_to_numpy=True)
    faiss.normalize_L2(chunk_embeddings)
    
    index = faiss.IndexFlatIP(chunk_embeddings.shape[1]) # Inner product for similarity
    index.add(chunk_embeddings)
    return index, chunks # Return the index and the chunks

def retrieve_similar_chunks(query, index, chunks, top_k=3):
    '''
    Retrieve the top k similar chunks to the query
    '''
    query_chunk = create_document_chunks([query], chunk_size=200)
    query_embedding = embedder.encode(query_chunk, convert_to_numpy=True)
    faiss.normalize_L2(query_embedding)
    
    k = min(len(chunks), top_k)
    distances, indices = index.search(query_embedding, k)
    return [chunks[i] for i in indices[0]] # return the top k chunks