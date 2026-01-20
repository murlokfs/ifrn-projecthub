from django.shortcuts import render
from django.views.generic import TemplateView


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

class DetalhesProjetosView(TemplateView):
    template_name = 'project/project_details.html'

class ComentariosAlunosView(TemplateView):
    template_name = 'project/student_comments.html'
    
class CadastroProjetoView(TemplateView):
    template_name = 'project/create_project.html'

class ComentariosProfessoresView(TemplateView):
    template_name = 'project/teacher_comments.html'
    
