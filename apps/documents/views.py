from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from core.services.document_service import DocumentService
from .serializers import DocumentSerializer


class UploadDocumentView(APIView):
    def post(self, request):
        file = request.FILES.get('file')

        if not file:
            return Response({"error": "No file provided"}, status=400)

        doc = DocumentService.upload_document(file)
        return Response(DocumentSerializer(doc).data, status=201)


class ListDocumentsView(APIView):
    def get(self, request):
        docs = DocumentService.list_documents()
        serializer = DocumentSerializer(docs, many=True)
        return Response(serializer.data)


class DeleteDocumentView(APIView):
    def delete(self, request, doc_id):
        try:
            DocumentService.delete_document(doc_id)
            return Response({"message": "Deleted successfully"})
        except Exception as e:
            return Response({"error": str(e)}, status=404)
