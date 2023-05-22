from django.http import HttpResponse
from django.db.models.query_utils import Q
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from django.core.mail import send_mail, BadHeaderError
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm


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


def logar_usuario(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('app:usuario_logado')
        else:
            form_login = AuthenticationForm()
    else:
        form_login = AuthenticationForm()
    return render(request, 'app/login/login.html', {'form_login': form_login})


@login_required(login_url='/logar_usuario')
def usuario_logado(request):
    return render(request, 'app/logado/logado.html')


@login_required(login_url='/logar_usuario')
def deslogar_usuario(request):
    logout(request)
    return redirect('app:index')


@login_required(login_url='/logar_usuario')
def alterar_senha(request):
    if request.method == 'POST':
        form_senha = PasswordChangeForm(request.user, request.POST)
        if form_senha.is_valid():
            user = form_senha.save()
            update_session_auth_hash(request, user)
            return redirect('app:index')
    else:
        form_senha = PasswordChangeForm(request.user)
    return render(request, 'app/altera_senha/alterar_senha.html', {'form_senha': form_senha})


def resetar_senha(request):
    if request.method == 'POST':
        resetar_senha_form = PasswordResetForm(request.POST)
        if resetar_senha_form.is_valid():
            data = resetar_senha_form.cleaned_data['email']
            associated_users = User.objects.filter(Q(username=data))
            if associated_users:
                for user in associated_users:
                    subject = 'Redefinição de senha solicitada'
                    email_template_name = 'app/recupera_senha/resetar_senha_email.txt'
                    context = {
                    'domain':'127.0.0.1:8000',
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': default_token_generator.make_token(user),
                    'protocol': 'http',
                    }
                    message = render_to_string(email_template_name, context)
                    print(message)
                    try:
                        send_mail(subject, message, 'admin@checknews.com', [user.email], fail_silently=False)
                    except BadHeaderError:
                        return HttpResponse('Cabeçalho inválido encontrado.')
                    return redirect ('app:password_reset_done')
    resetar_senha_form = PasswordResetForm()
    return render(request=request, template_name='app/recupera_senha/resetar_senha.html', context={'resetar_senha_form':resetar_senha_form})


@login_required(login_url='/logar_usuario')
def listagem(request):
    return render(request, 'app/listagem/listagem.html')


@login_required(login_url='/logar_usuario')
def checagem(request):
    return render(request, 'app/checagem/checagem.html')


@login_required(login_url='/logar_usuario')
def perfil(request):
    return render(request, 'app/perfil/perfil.html')


def sobre(request):
    return render(request, 'app/sobre/sobre.html')


@login_required(login_url='/logar_usuario')
def admin(request):
    return render(request, 'app/admin/admin.html')
