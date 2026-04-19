from apps.processing.models import TextChunk

class ChunkRepository:

    @staticmethod
    def create_chunk(document, chunk_text, embedding):
        return TextChunk.objects.create(
            document=document,
            chunk_text=chunk_text,
            embedding=embedding
        )

    @staticmethod
    def get_chunks_by_document(document):
        return TextChunk.objects.filter(document=document)