from rag.source_retriever import search_chunks_with_sources

question = "What is the procedure for applying for a student parking permit?"

results = search_chunks_with_sources(question, limit=5)

print("\nSEARCH RESULTS:\n")

if not results:
    print("No relevant document passages found.")

for result in results:
    print("Document:", result.get("title"))
    print("Section:", result.get("section_heading"))
    print("Page:", result.get("page_number"))
    print("Content:", result.get("chunk_text"))
    print("-" * 60)