from django.shortcuts import render
from django.views.generic import TemplateView
# Create your views here.

class PerfilView(TemplateView):
    template_name = 'authentication/perfil.html'
