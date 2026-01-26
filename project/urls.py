from django.urls import path
from project import views
from .views import DetalhesProjetosView, ComentariosAlunosView, ComentariosProfessoresView, ProjetosAprovacaoView,FeedView,SearchView,MeusProjetosView, delete_project, cancel_project_submission

urlpatterns = [

    path('project/details/<int:pk>/', DetalhesProjetosView.as_view(), name='project_details'),
    path('project/comments/<int:pk>/', ComentariosAlunosView.as_view(), name='project_comments'),
    path('create-project/', views.CadastroProjetoView.as_view(), name='create_project'),
    path('teacher-comments/<int:pk>/', ComentariosProfessoresView.as_view(), name='teacher_comments'),
    path('project-approval/', ProjetosAprovacaoView.as_view(), name='project_approval'),
    path('', FeedView.as_view(), name='index'),
    path('projects/', MeusProjetosView.as_view(), name='my_projects'),
    path('search/', SearchView.as_view(), name='search'),
    path('delete/<int:pk>/', delete_project, name='delete_project'),
    path('cancel-submission/<int:pk>/', cancel_project_submission, name='cancel_submission'),
]