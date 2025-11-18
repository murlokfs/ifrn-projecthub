from django.urls import path
from project import views
from .views import DetalhesProjetosView, ComentariosAlunosView, ComentariosProfessoresView

urlpatterns = [

    path('detalhes-projetos/', DetalhesProjetosView.as_view(), name='detalhes_projetos'),
    path('comentarios-alunos/', ComentariosAlunosView.as_view(), name='comentarios_alunos'),
    path('comentarios-professores/', ComentariosProfessoresView.as_view(), name='comentarios_professores'),
    path('', views.feed, name='index'),
    path('projects/', views.my_projects, name='my_projects'),
    path('popup/', views.popup, name='popup'),
]