from django.urls import path
from project import views
from .views import DetalhesProjetosView, ComentariosAlunosView, ComentariosProfessoresView, ProjetosAprovacaoView, DetalheProjetoPendenteProfessorView, FeedView,SearchView,MeusProjetosView, delete_project, cancel_project_submission, evaluate_project, complete_project, EditarProjetoView

urlpatterns = [

    path('project/details/<int:pk>/', DetalhesProjetosView.as_view(), name='project_details'),
    path('project/comments/<int:pk>/', ComentariosAlunosView.as_view(), name='project_comments'),
    path('create-project/', views.CadastroProjetoView.as_view(), name='create_project'),
    path('edit-project/<int:pk>/', EditarProjetoView.as_view(), name='edit_project'),
    path('teacher-comments/<int:pk>/', ComentariosProfessoresView.as_view(), name='teacher_comments'),
    path('project-approval/', ProjetosAprovacaoView.as_view(), name='project_approval'),
    path('project-details/pending/', DetalheProjetoPendenteProfessorView.as_view(), name='project_details_pending'),
#     path('', views.feed, name='index'),
#     path('projects/', views.my_projects, name='my_projects'),
    path('', FeedView.as_view(), name='index'),
    path('projects/', MeusProjetosView.as_view(), name='my_projects'),
    path('search/', SearchView.as_view(), name='search'),
    path('projects/delete/<int:pk>/', delete_project, name='delete_project'),
    path('projects/evaluate/<int:pk>/', evaluate_project, name='evaluate_project'),
    path('projects/complete/<int:pk>/', complete_project, name='complete_project'),
    path('cancel-submission/<int:pk>/', cancel_project_submission, name='cancel_submission'),
    path('api/search-entities/', views.search_entities, name='search_entities'),
]