import os
from core.repositories.document_repository import DocumentRepository
from apps.documents.models import Document
from core.services.content_extraction_service import ContentExtractionService
from core.repositories.content_repository import ContentRepository
from core.services.rag_service import RAGService
class DocumentService:

    @staticmethod
    def upload_document(file):
        name = file.name
        file_type = name.split('.')[-1]

        doc = DocumentRepository.create_document(file, name, file_type)

        file_path = doc.file.path

        extracted_text = ContentExtractionService.extract_text(file_path, file_type)

        ContentRepository.save_content(doc, extracted_text)

    # 🔥 NEW: RAG processing
        RAGService.process_document(doc, extracted_text)

        return doc

    @staticmethod
    def list_documents():
        return DocumentRepository.get_all_documents()

    @staticmethod
    def delete_document(doc_id):
        try:
            doc = Document.objects.get(id=doc_id)
        except Document.DoesNotExist:
            raise Exception("Document not found")

        # Delete file from storage
        if doc.file and os.path.isfile(doc.file.path):
            os.remove(doc.file.path)

        doc.delete()
        return True