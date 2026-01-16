from django.shortcuts import render
from django.views.generic import TemplateView

class PerfilView(TemplateView):
    template_name = 'authentication/profile.html'
    # passa active_page para que a sidebar marque a rota correta
    extra_context = {'active_page': 'perfil'}

class LoginView(TemplateView):
    template_name = 'authentication/login.html'

class SignupView(TemplateView):
    template_name = 'authentication/signup.html'

class EditProfileView(TemplateView):
    template_name = 'authentication/edit_profile.html'
