from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash

def index(request):
    return render(request, 'app/index.html', {'user': request.user})


def cadastrar_usuario(request):
    if request.method == 'POST':
        form_user = UserCreationForm(request.POST)
        if form_user.is_valid():
            form_user.save()
            return redirect('app:index')
    else:   
        form_user = UserCreationForm()
    return render(request, 'app/cadastro/cadastrar_usuario.html', {'form_user': form_user})


def login_usuario(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('app:usuario_logado')
        else:
            form_login = AuthenticationForm()
    else:
        form_login = AuthenticationForm()
    return render(request, 'app/login/login.html', {'form_login': form_login})


def usuario_logado(request):
    return render(request, 'app/logado/logado.html')


def deslogar_usuario(request):
    logout(request)
    return redirect('app:index')


def alterar_senha(request):
    if request.method == "POST":
        form_senha = PasswordChangeForm(request.user, request.POST)
        if form_senha.is_valid():
            user = form_senha.save()
            update_session_auth_hash(request, user)
            return redirect('index')
    else:
        form_senha = PasswordChangeForm(request.user)
    return render(request, 'alterar_senha.html', {'form_senha': form_senha})


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
