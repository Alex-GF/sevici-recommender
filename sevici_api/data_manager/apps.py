from django.apps import AppConfig


class DataManagerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'data_manager'
    
    def ready(self):
        from .sevici_API_updater import start
        start()
