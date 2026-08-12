"""
Vector Store
============
Handles embedding and storing document chunks in a local Chroma
vector database, and querying them by semantic similarity.
"""

import chromadb
from chromadb.utils import embedding_functions

# Persistent local storage — data survives between runs
CHROMA_PATH = "./chroma_db"

client = chromadb.PersistentClient(path=CHROMA_PATH)

# Uses a small, free, local embedding model (no API key needed)
embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"
)


def get_or_create_collection(collection_name: str):
    """
    Returns a Chroma collection for a given project/document set,
    creating it if it doesn't already exist.
    """
    return client.get_or_create_collection(
        name=collection_name,
        embedding_function=embedding_function,
    )


def add_chunks(collection_name: str, chunks: list[str], source: str) -> None:
    """
    Embeds and stores a list of text chunks in the given collection.

    Args:
        collection_name: Name of the Chroma collection (e.g. project id).
        chunks: List of text chunks to store.
        source: Name of the source document (e.g. filename), used for
                traceability of retrieved results.
    """
    collection = get_or_create_collection(collection_name)

    ids = [f"{source}_chunk_{i}" for i in range(len(chunks))]
    metadatas = [{"source": source} for _ in chunks]

    collection.add(
        ids=ids,
        documents=chunks,
        metadatas=metadatas,
    )


def query_similar_chunks(
    collection_name: str, query: str, top_k: int = 3
) -> list[dict]:
    """
    Finds the most semantically similar chunks to a query.

    Returns:
        A list of dicts, each containing 'text', 'source', and 'distance'.
    """
    collection = get_or_create_collection(collection_name)

    results = collection.query(
        query_texts=[query],
        n_results=top_k,
    )

    matches = []
    for i in range(len(results["documents"][0])):
        matches.append({
            "text": results["documents"][0][i],
            "source": results["metadatas"][0][i]["source"],
            "distance": results["distances"][0][i],
        })

    return matches
