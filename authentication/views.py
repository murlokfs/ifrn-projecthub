from django.shortcuts import render

# Create your views here.

def perfil(request):
    return render(request, 'authentication/perfil.html')