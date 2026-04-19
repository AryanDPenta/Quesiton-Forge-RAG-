from core.services.chunking_service import ChunkingService
from core.services.embedding_service import EmbeddingService
from core.repositories.chunk_repository import ChunkRepository
import numpy as np


class RAGService:

    @staticmethod
    def process_document(doc, extracted_text: str):
        print("🔥 RAG STARTED")

        if not extracted_text or extracted_text.strip() == "":
            print("❌ No extracted text found")
            return

        chunks = ChunkingService.chunk_text(extracted_text)

        print(f"📦 Total chunks created: {len(chunks)}")

        if len(chunks) == 0:
            print("❌ Chunking failed")
            return

        for i, chunk_text in enumerate(chunks):
            try:
                embedding = EmbeddingService.generate_embedding(chunk_text)

                ChunkRepository.create_chunk(
                    document=doc,
                    chunk_text=chunk_text,
                    embedding=embedding
                )

                print(f"✅ Chunk {i+1} stored")

            except Exception as e:
                print(f"❌ Error in chunk {i+1}: {str(e)}")

        print("🔥 RAG COMPLETED")

    # ---------------- Similarity ----------------
    @staticmethod
    def cosine_similarity(vec1, vec2):
        v1 = np.array(vec1)
        v2 = np.array(vec2)

        if np.linalg.norm(v1) == 0 or np.linalg.norm(v2) == 0:
            return 0

        return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))

    # ---------------- Retrieval ----------------
    @staticmethod
    def retrieve_relevant_chunks(query, document, top_k=3):
        print("🔍 Retrieval started")

        query_embedding = EmbeddingService.generate_embedding(query)

        chunks = ChunkRepository.get_chunks_by_document(document)

        print(f"📊 Total chunks in DB: {chunks.count()}")

        if not chunks.exists():
            print("❌ No chunks found for this document")
            return []

        scored = []

        for chunk in chunks:
            score = RAGService.cosine_similarity(query_embedding, chunk.embedding)
            scored.append((score, chunk.chunk_text))

        scored.sort(reverse=True, key=lambda x: x[0])

        top_chunks = [chunk for _, chunk in scored[:top_k]]

        print(f"✅ Retrieved {len(top_chunks)} chunks")

        return top_chunks