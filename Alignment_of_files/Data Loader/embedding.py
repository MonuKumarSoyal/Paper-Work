from scipy.spatial.distance import cosine
from sentence_transformers import SentenceTransformer

# Load the model
model = SentenceTransformer("johngiorgi/declutr-small")

# Prepare some text to embed
texts = [
    "A smiling costumed woman is holding an umbrella.",
    "A happy woman in a fairy costume holds an umbrella.",
]

# Embed the text
embeddings = model.encode(texts)
print(embeddings)
print(embeddings.shape)
semantic_sim = 1 - cosine(embeddings[0], embeddings[1])
print(semantic_sim)