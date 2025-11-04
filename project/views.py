from django.shortcuts import render

def feed(request):
    num_iterations = 6
    contador_list = range(num_iterations)
    show_status = False

    context = {
        "contador": num_iterations,
        "contador_list": contador_list,
        "show_status": show_status,
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
    }

    return render(request, 'project/my_projects.html', context)

def popup(request):
    return render(request, 'components/modals/types_projects/types_projects.html')