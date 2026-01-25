"""
Signals para o app de autenticação
"""
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User
from .tasks import send_welcome_email


@receiver(post_save, sender=User)
def user_post_save(sender, instance, created, **kwargs):
    """
    Signal disparado após salvar um usuário.
    Se é um novo usuário (created=True), envia email de boas-vindas.
    """
    if created:
        # Dispara a tarefa assíncrona para enviar o email
        send_welcome_email.delay(
            user_email=instance.email_personal,
            user_name=instance.full_name or instance.username
        )
