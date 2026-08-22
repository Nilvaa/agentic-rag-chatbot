from app.services.embedding_service import EmbeddingService

service=EmbeddingService()
text = "Employees must respect human rights."
embedding=service.generate_embedding(text)
print("Type:", type(embedding))
print("Dimensions:", len(embedding))
print("First 5 values:", embedding[:5])