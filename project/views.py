from django.shortcuts import render
from django.views.generic import TemplateView, CreateView, DetailView
from project.models import Project, ApprovalSolicitation, Tag
from project.forms import ProjectForm
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.db.models import Q
import re
from authentication.models import User


def feed(request):
    num_iterations = 6
    contador_list = range(num_iterations)
    show_status = False

    context = {
        "contador": num_iterations,
        "contador_list": contador_list,
        "show_status": show_status,
        "active_page": "feed",
    }

    return render(request, 'project/feed.html', context)

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
    context_object_name = 'project'
    template_name = 'project/project_details.html'

class ComentariosAlunosView(TemplateView):
    template_name = 'project/student_comments.html'
    
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
        # Usamos select_related para trazer os dados de curso e instituição em uma única consulta
        users = User.objects.filter(
            Q(full_name__icontains=query) | Q(registration__icontains=query),
            is_active=True
        ).select_related('course__institution')

        if entity_type == 'professor':
            users = users.filter(role='teacher') 
        elif entity_type == 'member':
            users = users.filter(role__in=['student', 'alumni']).exclude(id=request.user.id)

        data = []
        for u in users[:10]:
            # Pegamos a sigla da instituição e o campus dinamicamente
            if u.course and u.course.institution:
                # Exemplo: "IFPE • Campus Recife"
                info_text = f"{u.get_role_display()} • {u.course.institution.acronym} • {u.course.institution.campus}"
            else:
                info_text = f"{u.get_role_display()} • Instituição não informada"

            data.append({
                'id': u.id, 
                'name': u.full_name,
                'info': info_text, # Aqui vai o texto formatado dinamicamente
                'avatar_letter': u.full_name[0].upper() if u.full_name else '?'
            })

    return JsonResponse(data, safe=False)


class ComentariosProfessoresView(TemplateView):
    template_name = 'project/teacher_comments.html'

class ProjetosAprovacaoView(TemplateView):
    template_name = 'project/project_approvals.html'
    
