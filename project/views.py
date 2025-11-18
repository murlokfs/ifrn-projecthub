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
    num_iterations = 4
    contador_list = range(num_iterations)
    show_status = True

    context = {
        "contador": num_iterations,
        "contador_list": contador_list,
        "show_status": show_status,
        "active_page": "my_projects",
    }

    return render(request, 'project/my_projects.html', context)

class DetalhesProjetosView(TemplateView):
    template_name = 'project/detalhes_projetos.html'

class ComentariosAlunosView(TemplateView):
    template_name = 'project/comentarios_alunos.html'

class ComentariosProfessoresView(TemplateView):
    template_name = 'project/comentarios_professores.html'
    
def popup(request):
    return render(request, 'components/modals/awaiting_approval.html')
