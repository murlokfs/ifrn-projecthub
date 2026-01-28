from django.http import JsonResponse
from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .models import Project, Tag, ApprovalSolicitation, ReportProject
from project.forms import ProjectForm
from django.urls import reverse_lazy
import re
import json
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
            Q(members__username__icontains=query),
            is_active=True
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

        tab = self.request.GET.get('tab', 'trending') # Padrão é 'Em alta'
        if tab == 'my_campus' and self.request.user.is_authenticated:
            # Verifica se o usuário tem um curso vinculado
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

        project_type = self.request.GET.get('type')
        if project_type and project_type != 'all':
            queryset = queryset.filter(type=project_type)

        status = self.request.GET.get('status')
        if status and status != 'all':
            queryset = queryset.filter(status=status)

        tag_id = self.request.GET.get('tag')
        if tag_id and tag_id != 'all':
            queryset = queryset.filter(tags__id=tag_id)

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

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Project.objects.none()

        queryset = Project.objects.filter(Q(orientators=self.request.user) | Q(members=self.request.user), is_active=True)\
            .select_related('course')\
            .prefetch_related(
                'tags', 
                'members', 
                'approval_solicitations'
            ).order_by('-created_at')
        

        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) |
                Q(description__icontains=query) |
                Q(tags__name__icontains=query)
            ).distinct()

        status_filter = self.request.GET.get('status', 'all')
        
        if status_filter == 'approved':
            queryset = queryset.filter(
                Q(status='in_progress')
                | Q(status='completed')
                | Q(approval_solicitations__status='approved')
            ).distinct()
        
        elif status_filter in {'pending', 'pendant', 'pending_approval'}:
            queryset = queryset.filter(status='pending_approval').exclude(
                approval_solicitations__status='rejected'
            ).distinct()
        
        elif status_filter == 'reproved':
            queryset = queryset.filter(
                status='reproved',
            )
        
        elif status_filter == 'in_progress':
            queryset = queryset.filter(status='in_progress')
        
        elif status_filter == 'completed':
            queryset = queryset.filter(status='completed')

        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_page'] = 'my_projects'
        context['current_status'] = self.request.GET.get('status', 'all')
        context['search_query'] = self.request.GET.get('q', '')
        
        if self.request.user.is_authenticated:
            # Filtra apenas projetos ativos (is_active=True)
            user_projects = Project.objects.filter(
                Q(orientators=self.request.user) | Q(members=self.request.user),
                is_active=True
            ).prefetch_related('approval_solicitations')
            
            reproved_count = user_projects.filter(
                status='reproved',
            ).count()
            
            # Pendentes: pending_approval
            pending_count = user_projects.filter(
                status='pending_approval'
            ).count()
            
            # Aprovados: in_progress, completed OU com approval_solicitations.status='approved'
            # approved_count = user_projects.filter(
            #     Q(status='in_progress') | 
            #     Q(status='completed') |
            #     Q(approval_solicitations__status='approved')
            # ).distinct().count()

            in_progress_count = user_projects.filter(status='in_progress').count()
            completed_count = user_projects.filter(status='completed').count()
            all_count = user_projects.count()
            
            # context['approved_count'] = approved_count
            context['pending_count'] = pending_count
            context['reproved_count'] = reproved_count
            context['in_progress_count'] = in_progress_count
            context['completed_count'] = completed_count
            context['all_count'] = all_count
        
        return context

class DetalhesProjetosView(DetailView):
    model = Project
    context_object_name = 'project'
    template_name = 'project/project_details.html'

    def get_queryset(self):
        return (
            Project.objects.filter(is_active=True)
            .select_related('course')
            .prefetch_related('tags', 'members', 'orientators')
        )

class ComentariosAlunosView(DetailView):
    model = Project
    template_name = 'project/student_comments.html'
    context_object_name = 'project'
    
    def get_queryset(self):
        return Project.objects.filter(is_active=True)
    
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
            message="Projeto submetido para aprovação"
        )

        return response


@method_decorator(login_required, name='dispatch')
class EditarProjetoView(UpdateView):
    model = Project
    form_class = ProjectForm
    template_name = 'project/create_project.html'
    
    def get_object(self, queryset=None):
        return get_object_or_404(Project, pk=self.kwargs['pk'])
    
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        # Verifica se o usuário é membro do projeto
        if request.user not in self.object.members.all():
            messages.error(request, "Você não tem permissão para editar este projeto.")
            return redirect('my_projects')
        return super().get(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        # Verifica se o usuário é membro do projeto
        if request.user not in self.object.members.all():
            messages.error(request, "Você não tem permissão para editar este projeto.")
            return redirect('my_projects')
        return super().post(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object'] = self.object
        context['is_editing'] = True
        return context
    
    def get_success_url(self):
        return reverse_lazy('project_details', kwargs={'pk': self.object.pk})
    
    def form_valid(self, form):
        # Lógica para converter link do YouTube antes de salvar
        url = form.cleaned_data.get('link_youtube')
        if url:
            reg = r'^(?:https?://)?(?:www\.)?(?:youtu\.be/|youtube\.com/(?:embed/|v/|watch\?v=|watch\?.+&v=))((?:\w|-){11})(?:\S+)?$'
            match = re.search(reg, url)
            if match:
                video_id = match.group(1)
                form.instance.link_youtube = f'https://www.youtube.com/embed/{video_id}'
        
        # Mantém o curso original do projeto
        form.instance.course = self.object.course
        
        # Salva as alterações
        response = super().form_valid(form)
        
        # Se o projeto foi reprovado, cria nova solicitação de correção
        if self.object.status == 'reproved':
            # Desativa solicitações antigas
            ApprovalSolicitation.objects.filter(project=self.object, is_active=True).update(is_active=False)
            
            # Cria nova solicitação de correção
            ApprovalSolicitation.objects.create(
                project=self.object,
                user=self.request.user,
                message="Projeto corrigido e reenviado para aprovação",
                type='correction'
            )
            
            # Volta para status de pendente
            self.object.status = 'pending_approval'
            self.object.save()
            
            messages.success(self.request, "Projeto atualizado e reenviado para aprovação!")
        else:
            messages.success(self.request, "Projeto atualizado com sucesso!")
        
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

@method_decorator(login_required, name='dispatch')
class ProjetosAprovacaoView(ListView):
    model = Project
    template_name = 'project/project_approvals.html'
    context_object_name = 'projetos'
    paginate_by = 9

    def get_queryset(self):
        queryset = (
            Project.objects.filter(is_active=True, orientators=self.request.user.id).distinct()
        )

        # 🔍 Busca
        query = self.request.GET.get('q', '').strip()
        if query:
            queryset = queryset.filter(
                Q(title__icontains=query)
                | Q(description__icontains=query)
                | Q(tags__name__icontains=query)
                | Q(members__full_name__icontains=query)
                | Q(members__username__icontains=query)
            )

        # 🚦 Filtro por status (tabs)
        status_filter = self.request.GET.get('status', 'all')
        if status_filter == 'pending':
            queryset = queryset.filter(status='pending_approval')
        elif status_filter in {'in_progress', 'completed'}:
            queryset = queryset.filter(status=status_filter)
        else:
            queryset = queryset.exclude(status='pending_approval')

        return queryset.order_by('-created_at').distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_page'] = 'project_approval'
        context['current_status'] = self.request.GET.get('status', 'all')
        context['search_query'] = self.request.GET.get('q', '')

        base = Project.objects.filter(is_active=True, orientators=self.request.user.id).distinct()
        context['pending_count'] = base.filter(status='pending_approval').count()
        context['in_progress_count'] = base.filter(status='in_progress').count()
        context['completed_count'] = base.filter(status='completed').count()
        context['all_count'] = base.count()

        return context


@login_required
def delete_project(request, pk):
    """Deletar um projeto - soft delete em todos os casos (desativa sem apagar do banco)"""
    project = get_object_or_404(Project, pk=pk)
    user = request.user

    # --- CENÁRIO 1: O USUÁRIO É UM PROFESSOR (Docente) ---
    if user.role == 'teacher' or user.is_staff:
        # Professor: faz soft-delete de qualquer projeto
        project.is_active = False
        project.save()
        messages.success(request, "O projeto foi arquivado com sucesso.")
        return redirect('my_projects')

    # --- CENÁRIO 2: O USUÁRIO É DONO/MEMBRO (Aluno) ---
    elif user in project.members.all():
        # Aluno: faz soft-delete de seus projetos
        project.is_active = False
        project.save()
        messages.success(request, "O projeto foi desativado com sucesso.")
        return redirect('my_projects')

    # --- CENÁRIO 3: INTRUSO (Nem professor, nem dono) ---
    else:
        messages.error(request, "Você não tem permissão para realizar essa ação.")
        return redirect('my_projects')

class DetalheProjetoPendenteProfessorView(TemplateView):
    template_name = 'project/project_details.html'

    def dispatch(self, request, *args, **kwargs):
        # Temporariamente permitir acesso para todos os usuários
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Habilita o botão de aprovação no header
        context['show_approval_button'] = True
        user = getattr(self.request, 'user', None)
        context['is_teacher'] = bool(user and user.is_authenticated and getattr(user, 'role', None) == 'teacher')
        return context

@login_required
def cancel_project_submission(request, pk):
    """Cancel a project submission - desativa o projeto em vez de deletar"""
    project = get_object_or_404(Project, pk=pk)
    
    # Verifica se o usuário é membro do projeto
    if request.user not in project.members.all():
        messages.error(request, "Você não tem permissão para cancelar este projeto.")
        return redirect('my_projects')
    
    # Verifica se o projeto está em pendência
    if project.status != 'pending_approval':
        messages.error(request, "Apenas projetos em pendência de aprovação podem ser cancelados.")
        return redirect('my_projects')
    
    # Soft delete: desativa o projeto ao invés de deletar
    project.is_active = False
    project.save()
    
    messages.success(request, f'O projeto "{project.title}" foi cancelado e desativado com sucesso.')
    
    return redirect('my_projects')
    

@login_required
def evaluate_project(request, pk):
    """Processar avaliação de projeto (aprovação ou reprovação)"""
    if request.method != 'POST':
        return redirect('project_approval')
    
    project = get_object_or_404(Project, pk=pk)
    user = request.user
    
    # Verifica se o usuário é orientador do projeto
    if user not in project.orientators.all():
        messages.error(request, "Você não tem permissão para avaliar este projeto.")
        return redirect('project_approval')
    
    decision = request.POST.get('decision')
    feedback = request.POST.get('feedback', '').strip()
    
    # Validações
    if not decision or decision not in ['approve', 'reject']:
        messages.error(request, "Decisão inválida.")
        return redirect('project_approval')
    
    if not feedback:
        messages.error(request, "O feedback é obrigatório.")
        return redirect('project_approval')
    
    # Buscar ou criar solicitação de aprovação ativa
    solicitation = project.approval_solicitations.filter(is_active=True).first()
    
    if not solicitation:
        # Cria uma nova solicitação se não existir
        solicitation = ApprovalSolicitation.objects.create(
            project=project,
            user=project.members.first(),
            message=feedback,
            type='creation'
        )
    
    # Atualizar solicitação com feedback
    solicitation.message = feedback
    
    if decision == 'approve':
        solicitation.status = 'approved'
        solicitation.is_active = False
        project.status = 'in_progress'
        messages.success(request, f'Projeto "{project.title}" aprovado com sucesso!')
    else:  # reject
        solicitation.status = 'rejected'
        project.status = 'reproved'
        solicitation.is_active = False
        messages.warning(request, f'Projeto "{project.title}" foi reprovado. O aluno receberá o feedback.')
    
    solicitation.save()
    project.save()
    
    return redirect('project_approval')


@login_required
def complete_project(request, pk):
    """Marcar um projeto como concluído (só orientadores)"""
    if request.method != 'POST':
        return redirect('project_approval')
    
    project = get_object_or_404(Project, pk=pk)
    user = request.user
    
    # Verifica se o usuário é orientador do projeto
    if user not in project.orientators.all():
        messages.error(request, "Você não tem permissão para concluir este projeto.")
        return redirect('project_approval')
    
    # Verifica se o projeto está em desenvolvimento
    if project.status != 'in_progress':
        messages.error(request, "Apenas projetos em desenvolvimento podem ser concluídos.")
        return redirect('project_approval')
    
    # Altera o status do projeto
    project.status = 'completed'
    project.save()
    
    messages.success(request, f'Projeto "{project.title}" marcado como concluído com sucesso!')
    
    return redirect('project_approval')


@login_required
def deactivate_project_ajax(request, pk):
    """Desativar um projeto via AJAX - soft delete sem apagar do banco"""
    if request.method != 'POST':
        return JsonResponse({'success': False, 'message': 'Método não permitido'}, status=400)
    
    project = get_object_or_404(Project, pk=pk)
    user = request.user

    # --- Verificação de permissão ---
    # Professor ou staff podem desativar qualquer projeto
    if user.role == 'teacher' or user.is_staff:
        project.is_active = False
        project.save()
        return JsonResponse({
            'success': True, 
            'message': "O projeto foi arquivado com sucesso."
        })
    
    # Aluno pode desativar apenas seus próprios projetos
    elif user in project.members.all():
        project.is_active = False
        project.save()
        return JsonResponse({
            'success': True, 
            'message': "O projeto foi desativado com sucesso."
        })
    
    # Sem permissão
    else:
        return JsonResponse({
            'success': False, 
            'message': "Você não tem permissão para realizar essa ação."
        }, status=403)


@login_required
def report_project(request, pk):
    """Salvar denúncia de um projeto via AJAX"""
    if request.method != 'POST':
        return JsonResponse({'success': False, 'message': 'Método não permitido'}, status=400)
    
    project = get_object_or_404(Project, pk=pk)
    user = request.user
    
    # Obtém o motivo da denúncia do corpo da requisição
    import json
    try:
        data = json.loads(request.body)
        reason = data.get('reason', '').strip()
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'message': 'Dados inválidos'}, status=400)
    
    if not reason:
        return JsonResponse({'success': False, 'message': 'O motivo da denúncia é obrigatório'}, status=400)
    
    # Mapeamento de razões para textos amigáveis
    reason_map = {
        'plagio': 'Plágio',
        'inapropriado': 'Conteúdo Inapropriado',
        'falso': 'Informação Falsa'
    }
    
    reason_text = reason_map.get(reason, reason)
    
    # Verifica se o usuário já denunciou este projeto
    existing_report = ReportProject.objects.filter(
        project=project,
        user=user,
        is_resolved=False
    ).first()
    
    if existing_report:
        return JsonResponse({
            'success': False,
            'message': 'Você já denunciou este projeto. Aguarde análise da nossa equipe.'
        }, status=400)
    
    # Cria a denúncia
    report = ReportProject.objects.create(
        project=project,
        user=user,
        reason=reason_text
    )
    
    return JsonResponse({
        'success': True,
        'message': 'Denúncia enviada com sucesso! Nossa equipe irá analisar em breve.',
        'report_id': report.id
    })

