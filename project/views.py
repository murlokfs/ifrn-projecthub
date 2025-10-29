from django.shortcuts import render
# from authentication.models import User # Not used, can be removed
# from project.models import Projeto # Not used, can be removed

def my_projects(request):
    num_iterations = 4
    contador_list = range(num_iterations) # range(3) creates a range object from 0 to 2

    context = {
        "contador": num_iterations, # Keep this if you need the number itself for something else
        "contador_list": contador_list # The iterable to loop over
    }

    return render(request, 'project/my_projects.html', context)

def perfil(request):
    return render(request, 'project/perfil.html')
