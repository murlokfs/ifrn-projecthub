from django.urls import path
from project import views

urlpatterns = [
    path('', views.feed, name='index'),
    path('projects/', views.my_projects, name='my_projects'),
    # path('create_project/', views.create_project, name='create_project'),
]