from django.shortcuts import redirect, render
from django.contrib.auth import logout as auth_logout, login as auth_login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.views.generic import TemplateView
from django.contrib import messages
from .models import User


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


class EgressoLoginView(View):
    template_name = 'authentication/login_egresso.html'
    
    def get(self, request):
        return render(request, self.template_name)
    
    def post(self, request):
        email_personal = request.POST.get('email_personal', '').strip()
        password = request.POST.get('password', '').strip()
        
        if not email_personal or not password:
            messages.error(request, 'Email pessoal e senha são obrigatórios.')
            return render(request, self.template_name)
        
        try:
            user = User.objects.get(email_personal=email_personal)
            
            if user.check_password(password):
                auth_login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                return redirect('index')
            else:
                messages.error(request, 'Senha incorreta.')
                return render(request, self.template_name)
        except User.DoesNotExist:
            messages.error(request, 'Usuário não encontrado. Faça login pelo SUAP primeiro.')
            return render(request, self.template_name)
