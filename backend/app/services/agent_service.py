from app.services.retrieval_service import RetrievalService
from app.services.web_search_service import WebSearchService
from app.services.llm_service import LLMService


class AgentService:

    def __init__(self):
        self.retrieval_service = RetrievalService()
        self.web_search_service = WebSearchService()
        self.llm_service = LLMService()

    def run(
        self,
        question: str,
        db,
        history: str = ""
    ):

        print(f"\nUSER QUESTION: {question}")

        # ==================================================
        # STEP 1 — SEARCH UPLOADED DOCUMENTS
        # ==================================================

        results = self.retrieval_service.search(
            query=question,
            db=db,
            top_k=3
        )

        print(f"DOCUMENT RESULTS FOUND: {len(results)}")

        # ==================================================
        # STEP 2 — CHECK WHETHER DOCUMENT RESULTS ARE
        #          ACTUALLY RELEVANT
        # ==================================================

        relevant_results = []

        for chunk, filename, distance in results:

            print(
                f"Document: {filename} | "
                f"Page: {chunk.page_number} | "
                f"Distance: {distance}"
            )

            # Smaller distance = more similar
            #
            # This threshold may need adjustment depending
            # on your embedding/retrieval setup.
            if distance < 0.35:
                relevant_results.append(
                    (chunk, filename, distance)
                )

        # ==================================================
        # STEP 3 — DOCUMENT RAG
        # ==================================================

        if relevant_results:

            print("AGENT DECISION: DOCUMENTS")

            context = "\n\n".join(
                f"""
Source: {filename}
Page: {chunk.page_number}
Chunk: {chunk.chunk_index}

{chunk.content}
"""
                for chunk, filename, distance in relevant_results
            )

            answer = self.llm_service.generate_answer(
                question=question,
                context=context,
                history=history,
                source_type="document"
            )

            sources = [
                {
                    "type": "document",
                    "filename": filename,
                    "page": chunk.page_number,
                    "chunk": chunk.chunk_index
                }
                for chunk, filename, distance in relevant_results
            ]

            return {
                "tool": "documents",
                "answer": answer,
                "sources": sources
            }

        # ==================================================
        # STEP 4 — NO RELEVANT DOCUMENTS
        #          FALL BACK TO WEB SEARCH
        # ==================================================

        print("NO RELEVANT DOCUMENTS FOUND")
        print("AGENT DECISION: WEB")

        web_results = self.web_search_service.search(
            query=question,
            max_results=5
        )

        # ==================================================
        # STEP 5 — BUILD WEB CONTEXT
        # ==================================================

        web_context = "\n\n".join(
            f"""
Title: {result['title']}
URL: {result['url']}

{result['content']}
"""
            for result in web_results
        )

        # ==================================================
        # STEP 6 — GENERATE ANSWER FROM WEB
        # ==================================================

        answer = self.llm_service.generate_answer(
            question=question,
            context=web_context,
            history=history,
            source_type="web"
        )

        # ==================================================
        # STEP 7 — WEB SOURCES
        # ==================================================

        sources = [
            {
                "type": "web",
                "title": result["title"],
                "url": result["url"]
            }
            for result in web_results
        ]

        return {
            "tool": "web",
            "answer": answer,
            "sources": sources
        }