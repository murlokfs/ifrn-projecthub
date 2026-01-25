"""
Configuração do Celery para o projeto ifrn_projecthub
"""
import os
from celery import Celery

# Define o módulo de settings do Django para o programa 'celery'
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ifrn_projecthub.settings')

# Cria a instância do Celery
app = Celery('ifrn_projecthub')

# Carrega as configurações do Django com namespace 'CELERY'
app.config_from_object('django.conf:settings', namespace='CELERY')

# Descobre automaticamente as tarefas em todos os apps instalados
app.autodiscover_tasks()


@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
