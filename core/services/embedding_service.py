from sentence_transformers import SentenceTransformer

class EmbeddingService:
    model = SentenceTransformer('all-MiniLM-L6-v2')

    @staticmethod
    def generate_embedding(text):
        return EmbeddingService.model.encode(text).tolist()