from django.apps import AppConfig

class ProcessingConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.processing'          # ← This line must be 'apps.documents'
    verbose_name = "Processing"       # Optional, but nice