from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import ApprovalSolicitation

@receiver(post_save, sender=ApprovalSolicitation)
def automacao_aprovar_projeto(sender, instance, created, **kwargs):
    """
    Sempre que uma solicitação for salva:
    1. Se status for 'approved', muda o projeto para 'in_progress' e torna público.
    2. Se status for 'rejected', mantém pendente (ou faz outra lógica se quiser).
    """
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
        # --- LÓGICA DE REPROVAÇÃO (Opcional) ---
        print(f"⚠️ Solicitação Reprovada para projeto {projeto.id}.")
        # Aqui você pode, por exemplo, garantir que ele volte para rascunho
        # ou apenas deixar como está (Pendente) para o aluno ver a msg de erro.
        pass