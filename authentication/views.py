from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth import logout as auth_logout, login as auth_login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.views.generic import TemplateView, DetailView, UpdateView
from django.contrib import messages
from django.db.models import Q
from django.urls import reverse_lazy, reverse
from .models import User
from .forms import EditProfileForm
from project.models import Project


class LoginView(TemplateView):
    template_name = 'authentication/login.html'


class LogoutView(LoginRequiredMixin, View):
    login_url = 'login'
    
    def get(self, request):
        auth_logout(request)
        return redirect('login')


class PerfilView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'authentication/profile.html'
    context_object_name = 'profile_user'
    login_url = 'login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_visitado = self.object
        user_logado = self.request.user
        
        is_owner = (user_visitado == user_logado)
        context['is_owner'] = is_owner
        context['active_page'] = 'profile'
        
        # 1. Base da Query
        if is_owner:
            projetos = user_visitado.members.filter(is_active=True)
        else:
            projetos = user_visitado.members.filter(
                is_active=True,
                is_private=False,
                status__in=['in_progress', 'completed']
            )
        
        projetos = projetos.prefetch_related('tags', 'members')

        # 2. Filtro de Busca (Texto)
        query = self.request.GET.get('q', '').strip()
        if query:
            projetos = projetos.filter(
                Q(title__icontains=query) |
                Q(description__icontains=query) |
                Q(tags__name__icontains=query) |
                Q(members__full_name__icontains=query) |
                Q(members__username__icontains=query)
            ).distinct()

        # 3. Filtro de Status
        status_filter = self.request.GET.get('status', 'all')
        if status_filter and status_filter != 'all':
            projetos = projetos.filter(status=status_filter)

        # 4. Ordenação
        sort_by = self.request.GET.get('sort', 'newest')
        if sort_by == 'oldest':
            projetos = projetos.order_by('created_at')
        else:
            projetos = projetos.order_by('-created_at')

        context['projects_list'] = projetos
        context['published_projects'] = projetos  # Compatibilidade com template antigo
        context['total_projetos'] = projetos.count()
        
        context['current_filters'] = {
            'q': query,
            'status': status_filter,
            'sort': sort_by
        }
        
        # Compatibilidade com templates antigos
        context['current_status'] = status_filter
        context['sort_by'] = sort_by
        context['search_query'] = query
        
        return context


class SignupView(TemplateView):
    template_name = 'authentication/signup.html'


class EditProfileView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = EditProfileForm
    template_name = 'authentication/edit_profile.html'
    
    def get_object(self):
        return self.request.user

    def get_success_url(self):
        return reverse('profile', kwargs={'pk': self.object.pk})


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