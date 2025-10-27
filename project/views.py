# views.py

from django.shortcuts import render
# from authentication.models import User # Not used, can be removed
# from project.models import Projeto # Not used, can be removed

def my_projects(request):
    # Create a list of the desired length (e.g., [1, 2, 3])
    # The actual content of the list doesn't matter, only its length
    # A list comprehension is a clean way to do this.
    num_iterations = 4
    contador_list = range(num_iterations) # range(3) creates a range object from 0 to 2

    context = {
        "contador": num_iterations, # Keep this if you need the number itself for something else
        "contador_list": contador_list # The iterable to loop over
    }

    return render(request, 'project/my_projects.html', context)