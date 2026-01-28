from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import ApprovalSolicitation
from authentication.tasks import send_project_solicitation_email
from django.utils import timezone

@receiver(post_save, sender=ApprovalSolicitation)
def automacao_aprovar_projeto(sender, instance, created, **kwargs):
    # Só executa se tiver um projeto vinculado
    if not instance.project:
        return

    projeto = instance.project

    # Se for uma nova solicitação, envia email para os orientadores
    if created:
        # Pega todos os orientadores do projeto
        orientadores = projeto.orientators.all()
        
        # Formata a data da solicitação
        data_formatada = timezone.localtime(instance.created_at).strftime('%d/%m/%Y às %H:%M')
        
        # Envia email para cada orientador
        for orientador in orientadores:
            send_project_solicitation_email.delay(
                orientator_email=orientador.email,
                orientator_name=orientador.get_full_name() or orientador.username,
                project_title=projeto.title,
                project_type=projeto.type,
                student_name=instance.user.get_full_name() or instance.user.username,
                solicitation_message=instance.message,
                solicitation_date=data_formatada
            )

    if instance.status == 'approved':
        # --- LÓGICA DE APROVAÇÃO ---
        print(f"✅ Solicitação Aprovada! Atualizando projeto {projeto.id}...")
        
        # 1. Muda o status para Em Andamento
        projeto.status = 'in_progress'
        
        # Salva as alterações no banco
        projeto.save()
        
    elif instance.status == 'rejected':
        print(f"⚠️ Solicitação Reprovada para projeto {projeto.id}.")
        pass