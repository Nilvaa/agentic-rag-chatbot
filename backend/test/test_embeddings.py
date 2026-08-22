from sentence_transformers import SentenceTransformer

model=SentenceTransformer("BAAI/bge-small-en-v1.5")

text="Employees must respect human rights."

embedding=model.encode(text)

print("embedding type: ",type(embedding))
print("Embedding dimensions:",len(embedding))
print("First 5 values:",embedding[:5])