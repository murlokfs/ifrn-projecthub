from django.urls import path
from project import views
from .views import DetalhesProjetosView
from .views import ComentariosAlunosView
from .views import ComentariosProfessoresView
from .views import CadastroProjetoInstitucionalView
from .views import CadastroProjetoPesquisaView
from .views import CadastroProjetoTCCView
urlpatterns = [

    path('detalhes-projetos/', DetalhesProjetosView.as_view(), name='detalhes_projetos'),
    path('comentarios-alunos/', ComentariosAlunosView.as_view(), name='comentarios_alunos'),
    path('cadastro-projeto-institucional/', views.CadastroProjetoInstitucionalView.as_view(), name='cadastro_projeto_institucional'),
    path('cadastro-projeto-pesquisa/', views.CadastroProjetoPesquisaView.as_view(), name='cadastro_projeto_pesquisa'),
    path('cadastro-projeto-tcc/', views.CadastroProjetoTCCView.as_view(), name='cadastro_projeto_tcc'),
    path('comentarios-professores/', ComentariosProfessoresView.as_view(), name='comentarios_professores'),
    path('', views.feed, name='index'),
    path('projects/', views.my_projects, name='my_projects'),
    path('popup/', views.popup, name='popup'),
]