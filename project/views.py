from django.http import JsonResponse
from django.views import View
from django.shortcuts import render
from django.views.generic import TemplateView,ListView,DetailView
from django.db.models import Q
from .models import Project, Tag

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
            status__in=['in_progress', 'completed']
            #approval_solicitations__status='approved'
        ).select_related(
            'course__institution'
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











def my_projects(request):

    projetos = [
        {"status": "aprovado"},
        {"status": "pendente"},
        {"status": "reprovado"},
        {"status": "aprovado"},
    ]

    context = {
        "projetos": projetos,
        "active_page": "my_projects",
    }
    return render(request, "project/my_projects.html", context)

class DetalhesProjetosView(DetailView):
    model = Project
    template_name = 'project/project_details.html'
    context_object_name = 'project'

class ComentariosAlunosView(DetailView):
    model = Project
    template_name = 'project/student_comments.html'
    context_object_name = 'project'
    
class CadastroProjetoView(TemplateView):
    template_name = 'project/create_project.html'

class ComentariosProfessoresView(DetailView):
    model = Project
    template_name = 'project/teacher_comments.html'
    context_object_name = 'project'

class ProjetosAprovacaoView(TemplateView):
    template_name = 'project/project_approvals.html'
    
