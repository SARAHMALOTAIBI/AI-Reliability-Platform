from knowledge_base.document_loader import extract_text_from_pdf

pdf_path = "/Users/amira/Desktop/Teif AlHarthi CV Updated.pdf"

text = extract_text_from_pdf(pdf_path)

print(f"Extracted {len(text)} characters")
print("--- First 300 characters ---")
print(text[:300])


from knowledge_base.chunker import chunk_text

chunks = chunk_text(text)

print(f"\nTotal chunks: {len(chunks)}")
print("\n--- First chunk ---")
print(chunks[0])
print("\n--- Second chunk (notice overlap with end of first) ---")
print(chunks[1])


from knowledge_base.vector_store import add_chunks, query_similar_chunks

add_chunks(
    collection_name="test-collection",
    chunks=chunks,
    source="Teif_CV.pdf",
)

print("\n--- Chunks stored successfully ---")

results = query_similar_chunks(
    collection_name="test-collection",
    query="What programming languages does this person know?",
    top_k=2,
)

print("\n--- Query results ---")
for i, match in enumerate(results, 1):
    print(f"\nMatch {i} (distance: {match['distance']:.4f}):")
    print(match["text"][:200])


from knowledge_base.verification_agent import verify_answer

print("\n=== Test 1: Question WITH supporting info ===")
result1 = verify_answer(
    collection_name="test-collection",
    question="What programming languages does this person know?",
)
print(f"Is supported: {result1.is_supported}")
print(f"Explanation: {result1.explanation}")

print("\n=== Test 2: Question WITHOUT supporting info ===")
result2 = verify_answer(
    collection_name="test-collection",
    question="What is this person's favorite type of pizza?",
)
print(f"Is supported: {result2.is_supported}")
print(f"Explanation: {result2.explanation}")
