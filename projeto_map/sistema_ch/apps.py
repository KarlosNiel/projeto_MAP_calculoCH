from django.apps import AppConfig 


class SistemaChConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'sistema_ch'

    def ready(self):
        import sistema_ch.signals  # noqa F401
