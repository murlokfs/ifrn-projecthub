from django.urls import path
from project import views
from .views import DetalhesProjetosView, ComentariosAlunosView, ComentariosProfessoresView

urlpatterns = [

    path('project-details/', DetalhesProjetosView.as_view(), name='project_details'),
    path('student-comments/', ComentariosAlunosView.as_view(), name='student_comments'),
    path('create-project/', views.CadastroProjetoView.as_view(), name='create_project'),
    path('teacher-comments/', ComentariosProfessoresView.as_view(), name='teacher_comments'),
    path('', views.feed, name='index'),
    path('projects/', views.my_projects, name='my_projects'),
    path('api/search-entities/', views.search_entities, name='search_entities'),
]