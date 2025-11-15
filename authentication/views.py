from django.shortcuts import render
from django.views.generic import TemplateView
# Create your views here.

class PerfilView(TemplateView):
    template_name = 'authentication/perfil.html'
    # passa active_page para que a sidebar marque a rota correta
    extra_context = {'active_page': 'perfil'}
