from django.shortcuts import render
from django.views.generic import TemplateView

class PerfilView(TemplateView):
    template_name = 'authentication/perfil.html'

class LoginView(TemplateView):
    template_name = 'authentication/login.html'

class SignupView(TemplateView):
    template_name = 'authentication/signup.html'