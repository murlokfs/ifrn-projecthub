from django.shortcuts import redirect, render
from django.contrib.auth import logout as auth_logout, login as auth_login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.views.generic import TemplateView, ListView
from django.db.models import Q
from django.contrib import messages
from .models import User
from project.models import Project


class LoginView(TemplateView):
    template_name = 'authentication/login.html'


class LogoutView(LoginRequiredMixin, View):
    login_url = 'login'
    
    def get(self, request):
        auth_logout(request)
        return redirect('login')

class PerfilView(LoginRequiredMixin, ListView):
    template_name = 'authentication/profile.html'
    login_url = 'login'
    context_object_name = 'published_projects'
    paginate_by = 5

    def get_queryset(self):
        user = self.request.user
        queryset = (
            Project.objects.filter(
                is_active=True,
                is_private=False,
                status__in=['in_progress', 'completed'],
                members=user,
            )
            .prefetch_related('tags', 'members')
            .distinct()
        )

        # Filtro 1: status (tabs)
        status_filter = self.request.GET.get('status', 'all')
        if status_filter in {'in_progress', 'completed'}:
            queryset = queryset.filter(status=status_filter)

        # Busca
        query = self.request.GET.get('q', '').strip()
        if query:
            queryset = queryset.filter(
                Q(title__icontains=query)
                | Q(description__icontains=query)
                | Q(tags__name__icontains=query)
                | Q(members__full_name__icontains=query)
                | Q(members__username__icontains=query)
            )

        # Filtro 2: ordenação
        sort_by = self.request.GET.get('sort', 'newest')
        if sort_by == 'oldest':
            queryset = queryset.order_by('created_at')
        else:
            queryset = queryset.order_by('-created_at')

        return queryset.distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_page'] = 'profile'
        context['current_status'] = self.request.GET.get('status', 'all')
        context['sort_by'] = self.request.GET.get('sort', 'newest')
        context['search_query'] = self.request.GET.get('q', '')
        return context
class SignupView(TemplateView):
    template_name = 'authentication/signup.html'

class EditProfileView(TemplateView):
    template_name = 'authentication/edit_profile.html'
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
