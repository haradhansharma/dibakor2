from django.apps import AppConfig


class BdsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'bds'
    
    def ready(self):
        import bds.signals

