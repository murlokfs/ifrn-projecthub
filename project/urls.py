from django.urls import path
from project import views
from .views import DetalhesProjetosView

urlpatterns = [

    path('detalhes-projetos/', DetalhesProjetosView.as_view(), name='detalhes_projetos'),
 
    path('', views.feed, name='index'),
    path('projects/', views.my_projects, name='my_projects'),
    path('popup/', views.popup, name='popup'),
]