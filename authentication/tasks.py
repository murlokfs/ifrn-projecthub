"""
Tarefas assíncronas para o app de autenticação
"""
from celery import shared_task
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings


@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def send_welcome_email(self, user_email, user_name, user_id):
    try:
        context = {
            'user_first_name': user_name.split()[0] if user_name else '',
            'user_name': user_name,
            'site_name': 'PRISMA',
            'user_id': user_id
        }
        
        html_message = render_to_string('authentication/emails/welcome_email.html', context)
        plain_message = strip_tags(html_message)
        
        send_mail(
            subject=f'🧠 Bem-vindo ao PRISMA, {context["user_first_name"]}!',
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user_email],
            html_message=html_message,
            fail_silently=True,
        )
        
        return f'Email de boas-vindas enviado para {user_email}'
    
    except Exception as exc:
        raise self.retry(exc=exc)


@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def send_project_solicitation_email(self, orientator_email, orientator_name, project_title, 
                                   project_type, student_name, solicitation_message, solicitation_date):
    """
    Envia email para o orientador quando ele é vinculado a uma nova solicitação de projeto
    """
    try:
        project_types_pt = {
            'research': 'Pesquisa e Desenvolvimento',
            'integrator': 'Projeto Integrador',
            'thesis': 'Tese de Conclusão de Curso',
        }
        
        context = {
            'orientator_name': orientator_name,
            'orientator_first_name': orientator_name.split()[0] if orientator_name else '',
            'site_name': 'PRISMA',
            'project_title': project_title,
            'project_type': project_types_pt.get(project_type, project_type),
            'student_name': student_name,
            'solicitation_message': solicitation_message,
            'solicitation_date': solicitation_date,
        }
        
        html_message = render_to_string('authentication/emails/project_solicitation_email.html', context)
        plain_message = strip_tags(html_message)
        
        send_mail(
            subject=f'🧠 PRISMA - Nova Solicitação de Orientação - {project_title}',
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[orientator_email],
            html_message=html_message,
            fail_silently=True,
        )
        
        return f'Email de solicitação enviado para {orientator_email}'
    
    except Exception as exc:
        raise self.retry(exc=exc)


@shared_task
def send_notification_email(user_email, subject, message):
    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user_email],
            fail_silently=False,
        )
        return f'Email enviado para {user_email}'
    except Exception as e:
        return f'Erro ao enviar email: {str(e)}'
