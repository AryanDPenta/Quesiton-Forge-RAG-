from django.apps import AppConfig

class DocumentsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.documents'          # ← This line must be 'apps.documents'
    verbose_name = "Documents"       # Optional, but nice