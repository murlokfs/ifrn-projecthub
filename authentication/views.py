from django.shortcuts import redirect
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.views.generic import TemplateView


class LoginView(TemplateView):
    template_name = 'authentication/login.html'


class LogoutView(LoginRequiredMixin, View):
    login_url = 'login'
    
    def get(self, request):
        auth_logout(request)
        return redirect('login')


class PerfilView(LoginRequiredMixin, TemplateView):
    template_name = 'authentication/profile.html'
    login_url = 'login'
    extra_context = {'active_page': 'profile'}


class SignupView(TemplateView):
    template_name = 'authentication/signup.html'
