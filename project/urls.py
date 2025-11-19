from django.urls import path
from project import views
from .views import DetalhesProjetosView
from .views import ComentariosAlunosView
from .views import ComentariosProfessoresView
from .views import CadastroProjetoView

urlpatterns = [

    path('detalhes-projetos/', DetalhesProjetosView.as_view(), name='detalhes_projetos'),
    path('comentarios-alunos/', ComentariosAlunosView.as_view(), name='comentarios_alunos'),
    path('cadastro-projeto/', views.CadastroProjetoView.as_view(), name='cadastro_projeto'),
    path('comentarios-professores/', ComentariosProfessoresView.as_view(), name='comentarios_professores'),
    path('', views.feed, name='index'),
    path('projects/', views.my_projects, name='my_projects'),
    path('popup/', views.popup, name='popup'),
]