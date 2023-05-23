from os import getenv
from dotenv import load_dotenv
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

load_dotenv(verbose=True)


def index(request):
    return render(request, 'app/index.html', {'user': request.user})


def register_user(request):
    if request.method == 'POST':
        form_user = UserCreationForm(request.POST)
        if form_user.is_valid():
            form_user.save()
            return redirect('app:index')
    else:   
        form_user = UserCreationForm()
    return render(request, 'app/register/register_user.html', {'form_user': form_user})


def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('app:logged_user')
        else:
            form_login = AuthenticationForm()
    else:
        form_login = AuthenticationForm()
    return render(request, 'app/login/login.html', {'form_login': form_login})


@login_required(login_url='/login_user')
def logged_user(request):
    return render(request, 'app/logged/logged_user.html')


@login_required(login_url='/login_user')
def logout_user(request):
    logout(request)
    return redirect('app:index')


@login_required(login_url='/login_user')
def change_user_password(request):
    if request.method == 'POST':
        form_senha = PasswordChangeForm(request.user, request.POST)
        if form_senha.is_valid():
            user = form_senha.save()
            update_session_auth_hash(request, user)
            return redirect('app:index')
    else:
        form_senha = PasswordChangeForm(request.user)
    return render(request, 'app/change_password/change_user_password.html', {'form_senha': form_senha})


def password_reset(request):
    if request.method == 'POST':
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            associated_users = User.objects.filter(Q(username=data))
            if associated_users:
                for user in associated_users:
                    subject = 'Redefinição de senha solicitada'
                    email_template_name = 'app/recover_password/password_reset_email.txt'
                    context = {
                    'domain':'127.0.0.1:8000',
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': default_token_generator.make_token(user),
                    'protocol': 'http',
                    }
                    message = render_to_string(email_template_name, context)
                    from_email = getenv('EMAIL_HOST_USER')
                    print(from_email)

                    try:
                        send_mail(subject, message, from_email, [user.email], fail_silently=False)
                        print('Email enviado com sucesso.')
                    except BadHeaderError:
                        return HttpResponse('Cabeçalho inválido encontrado.')
                    return redirect ('app:password_reset_done')
    password_reset_form = PasswordResetForm()
    return render(request=request, template_name='app/recover_password/password_reset.html', context={'password_reset_form':password_reset_form})


@login_required(login_url='/login_user')
def news_listing(request):
    return render(request, 'app/listing/news_listing.html')


@login_required(login_url='/login_user')
def news_check(request):
    return render(request, 'app/check/news_check.html')


@login_required(login_url='/login_user')
def profile(request):
    return render(request, 'app/profile/profile.html')


@login_required(login_url='/login_user')
def admin(request):
    return render(request, 'app/admin/admin.html')


def about(request):
    return render(request, 'app/about/about.html')
