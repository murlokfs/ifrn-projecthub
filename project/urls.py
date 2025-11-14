from django.urls import path
from project import views
from .views import DetalhesProjetosView

urlpatterns = [
    path('', views.my_projects, name='index'),
    path('detalhes-projetos/', DetalhesProjetosView.as_view(), name='detalhes_projetos'),
]