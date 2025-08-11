from django.apps import AppConfig


class PlacementsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'placements'

    def ready(self):
        """Import signals when the app is ready"""
        import placements.signals 