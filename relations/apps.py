from django.apps import AppConfig


class RelationsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'relations'
    verbose_name = 'Партнёры'

    def ready(self):
        from . import signals
