from django.apps import AppConfig
import logging

logger = logging.getLogger(__name__)

class SistemaChConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'sistema_ch'

    def ready(self):
        try:
            import sistema_ch.signals  # Ativa os signals (Observer)
            logger.info("Signals do app 'sistema_ch' carregados com sucesso.")
        except ImportError as e:
            logger.error(f"Erro ao importar signals do app 'sistema_ch': {e}")
