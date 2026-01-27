from django.http import JsonResponse
from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView,ListView,DetailView,CreateView
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .models import Project, Tag,ApprovalSolicitation
from project.forms import ProjectForm
from django.urls import reverse_lazy
import re
from authentication.models import User
from django.contrib import messages

class SearchView(View):
    def get(self, request):
        query = request.GET.get('q', '').strip()

        if not query:
            return JsonResponse([], safe=False)

        projects = Project.objects.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(tags__name__icontains=query) |
            Q(members__full_name__icontains=query) |
            Q(members__username__icontains=query)
        ).distinct()

        data = [
            {
                "id": project.id,
                "title": project.title,
                "author": (
                    project.members.first().full_name
                    if project.members.exists()
                    else "Autor desconhecido"
                )
            }
            for project in projects
        ]

        return JsonResponse(data, safe=False)
class FeedView(ListView):
    model = Project
    template_name = 'project/feed.html'
    context_object_name = 'projects'
    paginate_by = 5

    def get_queryset(self):
        queryset = Project.objects.filter(
            is_private=False,
            is_active=True,
            status__in=['in_progress', 'completed']
            #approval_solicitations__status='approved'
        ).prefetch_related(
            'tags', 'members'
        ).distinct() # O distinct é importante para não duplicar o projeto se tiver mais de uma aprovação

        tab = self.request.GET.get('tab', 'trending') # Padrão é 'Em alta' (trending)

        if tab == 'my_campus' and self.request.user.is_authenticated:
            # Verifica se o usuário tem um curso vinculado
            # Ajuste 'course' se o nome do campo no seu User for diferente
            if hasattr(self.request.user, 'course') and self.request.user.course:
                user_institution = self.request.user.course.institution
                # Filtra projetos da MESMA instituição do usuário
                queryset = queryset.filter(course__institution=user_institution)

        # 🔍 BUSCA GLOBAL (HEADER)
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) |
                Q(description__icontains=query) |
                Q(tags__name__icontains=query) |
                Q(members__full_name__icontains=query) |
                Q(members__username__icontains=query)
            )

        # 📂 FILTRO POR TIPO
        project_type = self.request.GET.get('type')
        if project_type and project_type != 'all':
            queryset = queryset.filter(type=project_type)

        # 🚦 FILTRO POR STATUS
        status = self.request.GET.get('status')
        if status and status != 'all':
            queryset = queryset.filter(status=status)

        # 🏷️ FILTRO POR TAG
        tag_id = self.request.GET.get('tag')
        if tag_id and tag_id != 'all':
            queryset = queryset.filter(tags__id=tag_id)

        # 📅 ORDENAÇÃO
        sort_by = self.request.GET.get('sort', 'newest')  # Padrão: mais recentes
        if sort_by == 'oldest':
            queryset = queryset.order_by('created_at')
        else:
            queryset = queryset.order_by('-created_at')

        return queryset.distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['tags'] = Tag.objects.all()
        context['filters'] = self.request.GET
        context['search_query'] = self.request.GET.get('q', '')
        context['active_page'] = 'feed'
        context['current_tab'] = self.request.GET.get('tab', 'trending')
        context['sort_by'] = self.request.GET.get('sort', 'newest')

        return context

    def status_css_class(self):
        return {
        'pending_approval': 'outline-yellow',
        'in_progress': 'outline-blue',
        'completed': 'outline-green',
    }.get(self.status, '')

class MeusProjetosView(ListView):
    model = Project
    template_name = 'project/my_projects.html'
    context_object_name = 'projetos'
    paginate_by = 6

    # Garante que o usuário está logado
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Project.objects.none()
        
        # Busca projetos onde o usuário é membro
        queryset = Project.objects.filter(members=self.request.user, is_active=True)\
            .select_related('course')\
            .prefetch_related(
                'tags', 
                'members', 
                'approval_solicitations' # Traz as solicitações para mostrar o feedback
            ).order_by('-created_at')
        
        # --- Lógica de Busca (Barra de Pesquisa) ---
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) |
                Q(description__icontains=query) |
                Q(tags__name__icontains=query)
            ).distinct()

        # --- Lógica dos Botões de Filtro (Todos, Aprovado, Pendente...) ---
        status_filter = self.request.GET.get('status')
        if status_filter == 'approved':
            # Considera aprovado se tiver solicitação aprovada OU status concluído/em andamento
            queryset = queryset.filter(
                Q(status='in_progress') | 
                Q(status='completed') |
                Q(approval_solicitations__status='approved')
            ).distinct()
        elif status_filter == 'pendant':
            queryset = queryset.filter(status='pending_approval')
        elif status_filter == 'reproved':
            # Filtra projetos que têm UMA solicitação rejeitada e ainda estão pendentes
            queryset = queryset.filter(
                status='reproved',
            ).distinct()

        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_page'] = 'my_projects'
        # Passa os filtros atuais para o template (para manter o botão ativo se precisar)
        context['current_status'] = self.request.GET.get('status', 'all')
        context['search_query'] = self.request.GET.get('q', '')
        
        # Contar projetos por status (sem duplicação)
        if self.request.user.is_authenticated:
            user_projects = Project.objects.filter(members=self.request.user).prefetch_related('approval_solicitations')
            
            # Reprovados: projetos que têm approval_solicitations com status='rejected'
            reproved_projects = set()
            for project in user_projects:
                if project.approval_solicitations.filter(status='rejected').exists():
                    reproved_projects.add(project.id)
            reproved_count = len(reproved_projects)
            
            # Pendentes: pending_approval E que NÃO estão em reprovados
            pending_count = user_projects.filter(
                status='pending_approval'
            ).exclude(id__in=reproved_projects).count()
            
            # Aprovados: in_progress, completed OU com approval_solicitations.status='approved'
            # E que NÃO estão em reprovados
            approved_count = user_projects.filter(
                Q(status='in_progress') | 
                Q(status='completed') |
                Q(approval_solicitations__status='approved')
            ).exclude(id__in=reproved_projects).distinct().count()
            
            context['approved_count'] = approved_count
            context['pending_count'] = pending_count
            context['reproved_count'] = reproved_count
        
        return context











class DetalhesProjetosView(DetailView):
    model = Project
    context_object_name = 'project'
    template_name = 'project/project_details.html'

class ComentariosAlunosView(DetailView):
    model = Project
    template_name = 'project/student_comments.html'
    context_object_name = 'project'
    
class CadastroProjetoView(CreateView):
    model = Project
    form_class = ProjectForm
    template_name = 'project/create_project.html'
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        # Lógica para converter link do YouTube antes de salvar
        url = form.cleaned_data.get('link_youtube')
        if url:
            # Expressão regular para capturar o ID do vídeo
            reg = r'^(?:https?://)?(?:www\.)?(?:youtu\.be/|youtube\.com/(?:embed/|v/|watch\?v=|watch\?.+&v=))((?:\w|-){11})(?:\S+)?$'
            match = re.search(reg, url)
            if match:
                video_id = match.group(1)
                # Salva no formato embed para evitar Erro 153 futuramente
                form.instance.link_youtube = f'https://www.youtube.com/embed/{video_id}'

        # adicionando o curso do usuario logado no projeto
        form.instance.course = self.request.user.course
        response = super().form_valid(form)

        self.object.members.add(self.request.user)

        # Cria solicitação de aprovação
        ApprovalSolicitation.objects.create(
            project=self.object,
            user=self.request.user, 
        )

        return response

def search_entities(request):
    query = request.GET.get('q', '')
    entity_type = request.GET.get('type', '')

    if not query or len(query) < 2:
        return JsonResponse([], safe=False)

    if entity_type == 'tag':
        results = Tag.objects.filter(name__icontains=query)[:15]
        data = [{'id': t.id, 'name': t.name} for t in results]
    
    else:
        users = User.objects.filter(
            Q(full_name__icontains=query) | Q(registration__icontains=query) | Q(username__icontains=query),
            is_active=True
        ).select_related('course__campus')

        if entity_type == 'professor':
            users = users.filter(role='teacher') 
        elif entity_type == 'member':
            users = users.filter(role='student').exclude(id=request.user.id)

        data = []
        for u in users[:10]:
            if u.course and u.course.campus:
                info_text = f"{u.get_role_display()} • {u.course.campus.name}"
            else:
                info_text = f"{u.get_role_display()} • Campus não informado"

            data.append({
                'id': u.id, 
                'name': u.full_name,
                'info': info_text,
                'avatar_letter': u.full_name[0].upper() if u.full_name else '?'
            })

    return JsonResponse(data, safe=False)


class ComentariosProfessoresView(DetailView):
    model = Project
    template_name = 'project/teacher_comments.html'
    context_object_name = 'project'

class ProjetosAprovacaoView(TemplateView):
    template_name = 'project/project_approvals.html'


@login_required
def delete_project(request, pk):
    """Delete a project if the user is a member"""
    project = get_object_or_404(Project, pk=pk)
    
    # Verifica se o usuário é membro do projeto
    if request.user not in project.members.all():
        return redirect('my_projects')
    
    # Delete the project
    project.delete()
    
    # Redirect back to my_projects
    return redirect('my_projects')


@login_required
def cancel_project_submission(request, pk):
    """Cancel a project submission (change status from pending_approval back to draft)"""
    project = get_object_or_404(Project, pk=pk)
    
    # Verifica se o usuário é membro do projeto
    if request.user not in project.members.all():
        return redirect('my_projects')
    
    # Only cancel if project is in pending_approval status
    if project.status == 'pending_approval':
        project.status = 'draft'
        project.save()
    
    return redirect('my_projects')
    

@login_required
def delete_project(request, pk):
    project = get_object_or_404(Project, pk=pk)
    user = request.user
    
    # Verifica se o projeto já passou da fase de pendente (Aprovado, Em andamento ou Concluído)
    is_approved_or_started = project.status != 'pending_approval'

    # --- CENÁRIO 1: O USUÁRIO É UM PROFESSOR (Docente) ---
    if user.role == 'teacher' or user.is_staff:
        if is_approved_or_started:
            # Regra: Professor faz "Soft Delete" em projetos aprovados
            project.is_active = False
            project.save()
            messages.success(request, "O projeto foi arquivado com sucesso.")
        else:
            # Se for pendente, o professor pode apagar permanentemente
            project.delete()
            messages.success(request, "Projeto pendente excluído permanentemente.")
        
        return redirect('my_projects')

    # --- CENÁRIO 2: O USUÁRIO É DONO/MEMBRO (Aluno) ---
    elif user in project.members.all():
        if is_approved_or_started:
            # Regra: Aluno NÃO pode excluir projeto aprovado
            messages.error(request, "Projetos aprovados não podem ser excluídos. Entre em contato com um professor.")
        else:
            # Se for pendente, aluno pode apagar permanentemente (ex: desistiu da ideia)
            project.delete()
            messages.success(request, "Projeto excluído com sucesso.")
            
        return redirect('my_projects')

    # --- CENÁRIO 3: INTRUSO (Nem professor, nem dono) ---
    else:
        messages.error(request, "Você não tem permissão para realizar essa ação.")
        return redirect('my_projects')