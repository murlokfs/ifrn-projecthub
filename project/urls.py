from django.urls import path
from project import views

urlpatterns = [
    path('', views.my_projects, name='my_projects'),
]