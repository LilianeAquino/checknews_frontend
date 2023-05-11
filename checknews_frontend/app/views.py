from django.shortcuts import render


def index(request):
    return render(request, 'app/index.html')


def login(request):
    return render(request, 'app/login/login.html')


def listagem(request):
    return render(request, 'app/listagem/listagem.html')


def checagem(request):
    return render(request, 'app/checagem/checagem.html')


def perfil(request):
    return render(request, 'app/perfil/perfil.html')


def sobre(request):
    return render(request, 'app/sobre/sobre.html')


def admin(request):
    return render(request, 'app/admin/admin.html')
