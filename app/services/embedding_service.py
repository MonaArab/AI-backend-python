from sentence_transformers import SentenceTransformer


class EmbeddingService:

    def __init__(self):
        self.model = SentenceTransformer(
            "sentence-transformers/all-MiniLM-L6-v2"
        )

    def generate_embedding(
        self,
        text: str
    ) -> list[float]:

        embedding = self.model.encode(text)

        return embedding.tolist()
