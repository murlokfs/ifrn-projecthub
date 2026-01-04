from django.urls import path
from project import views

urlpatterns = [

    path('project-details/<int:pk>/', views.DetailsProject.as_view(), name='project_details'),
    path('student-comments/', views.ComentariosAlunosView.as_view(), name='student_comments'),
    path('create-project/', views.CadastroProjetoView.as_view(), name='create_project'),
    path('teacher-comments/', views.ComentariosProfessoresView.as_view(), name='teacher_comments'),
    path('', views.Feed.as_view(), name='index'),
    path('projects/', views.My_projects.as_view(), name='my_projects'),
]