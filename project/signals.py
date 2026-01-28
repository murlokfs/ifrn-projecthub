from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import ApprovalSolicitation

@receiver(post_save, sender=ApprovalSolicitation)
def automacao_aprovar_projeto(sender, instance, created, **kwargs):
    # Só executa se tiver um projeto vinculado
    if not instance.project:
        return

    projeto = instance.project

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