from apps.processing.models import ExtractedContent


class ContentRepository:

    @staticmethod
    def save_content(document, text):
        return ExtractedContent.objects.create(
            document=document,
            content=text
        )

    @staticmethod
    def get_content_by_document(document):
        return ExtractedContent.objects.get(document=document)