from django.urls import path
from .views import UploadDocumentView, ListDocumentsView, DeleteDocumentView

urlpatterns = [
    path('upload/', UploadDocumentView.as_view()),
    path('', ListDocumentsView.as_view()),
    path('<int:doc_id>/', DeleteDocumentView.as_view()),
]