from django.urls import path
from project import views
from .views import DetalhesProjetosView, ComentariosAlunosView, ComentariosProfessoresView, ProjetosAprovacaoView,FeedView,SearchView

urlpatterns = [

    path('project-details/<int:pk>/', DetalhesProjetosView.as_view(), name='project_details'),
    path('student-comments/', ComentariosAlunosView.as_view(), name='student_comments'),
    path('create-project/', views.CadastroProjetoView.as_view(), name='create_project'),
    path('teacher-comments/', ComentariosProfessoresView.as_view(), name='teacher_comments'),
    path('project-approval/', ProjetosAprovacaoView.as_view(), name='project_approval'),
    path('', FeedView.as_view(), name='index'),
    path('projects/', views.my_projects, name='my_projects'),
    path('search/', SearchView.as_view(), name='search'),
]