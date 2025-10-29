from django.urls import path
from authentication import views

urlpatterns = [
    path('perfil/', views.perfil, name='perfil'),
]