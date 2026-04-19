from django.db import models
from apps.documents.models import Document


class ExtractedContent(models.Model):
    document = models.OneToOneField(Document, on_delete=models.CASCADE)
    content = models.TextField()

    def __str__(self):
        return f"Content for {self.document.name}"

class TextChunk(models.Model):
    document = models.ForeignKey(Document, on_delete=models.CASCADE)
    chunk_text = models.TextField()
    embedding = models.JSONField()

    def __str__(self):
        return f"Chunk for {self.document.name}"