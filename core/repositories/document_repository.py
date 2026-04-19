from apps.documents.models import Document

class DocumentRepository:

    @staticmethod
    def create_document(file, name, file_type):
        return Document.objects.create(
            file=file,
            name=name,
            file_type=file_type
        )

    @staticmethod
    def get_all_documents():
        return Document.objects.all().order_by('-uploaded_at')

    @staticmethod
    def delete_document(doc_id):
        doc = Document.objects.get(id=doc_id)
        doc.delete()