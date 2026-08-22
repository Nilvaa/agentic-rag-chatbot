from app.database import SessionLocal

from app.services.retrieval_service import RetrievalService
from app.services.llm_service import LLMService


db = SessionLocal()

try:

    question = "What does Apple say about human rights?"

    # 1. Retrieve relevant chunks
    retrieval_service = RetrievalService()

    results = retrieval_service.search(
        query=question,
        db=db,
        top_k=3
    )

    # 2. Display retrieved chunks
    print("\nRetrieved Chunks:")
    print("=" * 60)

    for chunk, filename, distance in results:

        print(f"Document    : {filename}")
        print(f"Document ID : {chunk.document_id}")
        print(f"Page        : {chunk.page_number}")
        print(f"Chunk       : {chunk.chunk_index}")
        print(f"Distance    : {distance}")
        print(f"Content     : {chunk.content}")

    print("-" * 60)

    # 3. Build context
    context = "\n\n".join(
    f"""
    Source: {filename}
    Page: {chunk.page_number}
    Chunk: {chunk.chunk_index}

    {chunk.content}
        """
    for chunk, filename, distance in results
)

    # 4. Generate answer using Ollama
    llm_service = LLMService()

    answer = llm_service.generate_answer(
        question=question,
        context=context
    )

    # 5. Display final answer
    print("\nFinal Answer:")
    print("=" * 60)
    print(answer)

    #display source
    print("\nSources:")
    print("=" * 60)

    for chunk,filename,distance in results:
        print(
        f"- {filename} | "
        f"Page {chunk.page_number} | "
        f"Chunk {chunk.chunk_index}"
    )

finally:
    db.close()