from django.apps import AppConfig


class AuthenticationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'authentication'

    def ready(self):
        """
        Importa os signals quando o app estiver pronto
        """
        import authentication.signals
