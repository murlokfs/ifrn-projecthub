from django.shortcuts import render

def my_projects(request):
    num_iterations = 4
    contador_list = range(num_iterations)

    context = {
        "contador": num_iterations,
        "contador_list": contador_list
    }

    return render(request, 'project/my_projects.html', context)

