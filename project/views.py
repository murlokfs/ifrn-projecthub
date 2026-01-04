from django.shortcuts import render
from django.views import generic
from authentication.models import User
from project.models import Project
from django.db.models import Case, When, Value, IntegerField

class Feed(generic.ListView):
    model = Project
    template_name = 'project/feed.html'
    context_object_name = 'projects'
    paginate_by = 2

    def get_queryset(self):
        return Project.objects.filter(
            status='Aprovado'
        ).distinct().order_by('-id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['show_status'] = False
        context['active_page'] = 'feed'
        return context

class My_projects(generic.ListView):
    model = Project
    template_name = 'project/my_projects.html'
    context_object_name = 'projects'
    paginate_by = 9

    def get_queryset(self):
        user = User.objects.get(id=1)  # temporário
        return Project.objects.filter(members=user).distinct().annotate(
            search_priority=Case(
                When(status='Aprovado', then=Value(1)),
                When(status='Pendente', then=Value(2)),
                When(status='Reprovado', then=Value(3)),
                default=Value(4),
                output_field=IntegerField(),
            )
        ).order_by('search_priority', '-id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = User.objects.get(id=1)
        
        # Filtramos o queryset do usuário e contamos cada status
        user_projects = Project.objects.filter(members=user)
        
        context['count_aprovados'] = user_projects.filter(status='Aprovado').count()
        context['count_pendentes'] = user_projects.filter(status='Pendente').count()
        context['count_reprovados'] = user_projects.filter(status='Reprovado').count()
        
        context['show_status'] = True
        context['active_page'] = 'my_projects'
        return context

class DetailsProject(generic.DetailView):
    model = Project
    template_name = 'project/project_details.html'

class ComentariosAlunosView(generic.TemplateView):
    template_name = 'project/student_comments.html'
    
class CadastroProjetoView(generic.TemplateView):
    template_name = 'project/create_project.html'

class ComentariosProfessoresView(generic.TemplateView):
    template_name = 'project/teacher_comments.html'
    
