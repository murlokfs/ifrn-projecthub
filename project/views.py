from django.shortcuts import render
from django.views import generic
from authentication.models import User
from project.models import Project

class Feed(generic.ListView):
    model = Project
    template_name = 'project/feed.html'
    context_object_name = 'projects'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['show_status'] = False
        context['active_page'] = 'feed'
        return context

class My_projects(generic.ListView):
    model = Project
    template_name = 'project/my_projects.html'
    context_object_name = 'projects'

    def get_queryset(self):
        user = User.objects.get(id=1)  # temporário
        return Project.objects.filter(
            members=user
        ).distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['show_status'] = True
        context['active_page'] = 'my_projects'
        return context

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

class DetalhesProjetosView(generic.TemplateView):
    template_name = 'project/project_details.html'

class ComentariosAlunosView(generic.TemplateView):
    template_name = 'project/student_comments.html'
    
class CadastroProjetoView(generic.TemplateView):
    template_name = 'project/create_project.html'

class ComentariosProfessoresView(generic.TemplateView):
    template_name = 'project/teacher_comments.html'
    
