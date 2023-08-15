import csv
import requests
import pymongo
from os import getenv
from bs4 import BeautifulSoup
import smtplib
from smtplib import SMTPException
from datetime import datetime, timedelta
from dotenv import load_dotenv
from django.conf import settings
from django.http import HttpResponse
from django.contrib import messages
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
from app.models import FakeNewsDetection, FeedbackUser, FakeNewsDetectionDetail, Ticket, Tips, Chat


load_dotenv(verbose=True)


client = pymongo.MongoClient(getenv('URL_MONGO'))
dbname = client[getenv('DB_NAME')]


def index(request):
    return render(request, 'app/index.html', {'user': request.user})


def register_user(request):
    if request.method == 'POST':
        form_user = UserCreationForm(request.POST)
        if form_user.is_valid():
            form_user.save()
            messages.success(request, 'Cadastro realizado com sucesso! Você já pode fazer login.')
            return redirect('app:login_user')
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

            if user.is_staff:
                return redirect('app:admin')
            return redirect('app:logged_user')
        else:
            messages.error(request, 'Email ou senha inválidos')
            form_login = AuthenticationForm()
    else:
        form_login = AuthenticationForm()
    return render(request, 'app/login/login.html', {'form_login': form_login})


def login_google(request):
    tips = Tips.objects.all()
    return render(request, 'app/logged/logged_user.html', {'tips': tips})


@login_required(login_url='/login_user')
def logged_user(request):
    tips = Tips.objects.all()
    return render(request, 'app/logged/logged_user.html', {'tips': tips})


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
            return redirect('app:login_user')
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
                    from_email = settings.EMAIL_HOST_USER
                    try:
                        send_mail(subject, message, from_email, [user.username], fail_silently=False, html_message=message)
                        print('Email enviado com sucesso.')
                    except BadHeaderError:
                        return HttpResponse('Cabeçalho inválido encontrado.')
                    except SMTPException as e:
                        print(f"Erro ao enviar o email: {e}")
                        return HttpResponse('Ocorreu um erro ao enviar o email.')
                    return redirect ('app:password_reset_done')
    password_reset_form = PasswordResetForm()
    return render(request=request, template_name='app/recover_password/password_reset.html', context={'password_reset_form':password_reset_form})


@login_required(login_url='/login_user')
def news_check(request):
    return render(request, 'app/check/news_check.html')


@login_required(login_url='/login_user')
def process_form_news(request):
    if request.method == 'POST':
        link = request.POST.get('url')
        response = requests.get(link)

        soup = BeautifulSoup(response.content, 'html.parser')
        text = soup.get_text()

        discard_terms = ['YouTube', 'JavaScript is not available']
        discard = any(term in text for term in discard_terms)

        if discard or text is None:
            classification = 'Texto não extraido'
            result_check = FakeNewsDetection(link=link, content=text, classification=classification, user_id=int(request.user.id))
        else:
            api_endpoint = getenv('URL_BACKEND')
            payload = {'text': text, 'origin': link}
            response = requests.post(api_endpoint, json=payload)
            data = response.json()

            confidence = data['classification']['confianca']
            classification = data['classification']['label']        
            result_check = FakeNewsDetection(link=link, content=text, classification=classification, confidence=confidence, user_id=int(request.user.id))

        result_check.save()
        return redirect('app:checked_news')
    else:
        return render(request, 'app/check/news_check.html')


@login_required(login_url='/login_user')
def news_detail(request, news_id):
    news = FakeNewsDetection.objects.get(id=news_id)
    return render(request, 'app/check/news_detail.html', {'news': news})


@login_required(login_url='/login_user')
def process_form_news_details(request, news_id):
    news = FakeNewsDetection.objects.get(id=news_id)

    if request.method == 'POST':
        is_favorite = request.POST.get('favorite') == 'on'
        tags = request.POST.get('tags')
        review = request.POST.get('review')
        detail = FakeNewsDetectionDetail(news=news, is_favorite=is_favorite, tags=tags, review=float(review))
        detail.save()
    return redirect('app:checked_news')


@login_required(login_url='/login_user')
def checked_news(request):
    collection = dbname[getenv('COLLECTION_FAKE_NEWS_DETECTION')]
    dado = collection.find().sort('_id', -1).limit(1)[0]
    dado['confidence'] = dado['confidence'].to_decimal() * 100
    return render(request, 'app/check/checked_news.html', {'dado': dado})


@login_required(login_url='/login_user')
def news_listing(request):
    collection = dbname[getenv('COLLECTION_FAKE_NEWS_DETECTION')]
    detalhes_collection = dbname[getenv('COLLECTION_FAKE_NEWS_DETECTION_DETAILS')]

    data_minima = datetime.now() - timedelta(days=7)
    data_formatada = data_minima.strftime('%d/%m/%Y')
    user = request.user

    if user.is_staff:
        documentos = list(collection.find({'date': {'$gte': datetime.strptime(data_formatada, '%d/%m/%Y')}}))
    else:
        documentos = list(collection.find({'user_id': int(user.id), 'date': {'$gte': datetime.strptime(data_formatada, '%d/%m/%Y')}}))

    for documento in documentos:
        documento['confidence'] = documento['confidence'].to_decimal() * 100
        detalhes = detalhes_collection.find_one({'news_id': documento['id']})
        
        if detalhes is not None:
            documento['tags'] = detalhes.get('tags')
            documento['is_favorite'] = detalhes.get('is_favorite')
            documento['review'] = detalhes.get('review')
        else:
            documento['tags'] = None
            documento['is_favorite'] = False
            documento['review'] = 'sem nota'
    return render(request, 'app/listing/news_listing.html', {'documentos': documentos})


@login_required(login_url='/login_user')
def generate_report_news(request):
    collection = dbname[getenv('COLLECTION_FAKE_NEWS_DETECTION')]
    detalhes_collection = dbname[getenv('COLLECTION_FAKE_NEWS_DETECTION_DETAILS')]
    user = request.user

    if user.is_staff:
        documentos = list(collection.find({}))
    else:
        documentos = list(collection.find({'user_id': int(user.id)}))

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="relatorio_noticias_analisadas.csv"'

    writer = csv.writer(response)
    writer.writerow(['data', 'link', 'noticia', 'resultado', '% de confianca', 'tags', 'favoritos', 'notas'])

    for documento in documentos:
        detalhes_documento = detalhes_collection.find_one({'news_id': documento['id']})
        if detalhes_documento:
            favoritos = detalhes_documento['is_favorite']
            tags = detalhes_documento['tags']
            reviews = detalhes_documento['review']
        else:
            favoritos = None
            tags = None
            reviews = None
        documento['confidence'] = round(documento['confidence'].to_decimal() * 100, 2)
        writer.writerow([documento['date'], documento['link'], documento['content'], documento['classification'], documento['confidence'], tags, favoritos, reviews])   
    return response


@login_required(login_url='/login_user')
def users_listing(request):
    collection = dbname[getenv('COLLECTION_USERS')]
    usuarios = list(collection.find({}))
    return render(request, 'app/listing/users_listing.html', {'usuarios':usuarios})


@login_required(login_url='/login_user')
def generate_report_users(request):
    collection = dbname[getenv('COLLECTION_USERS')]

    usuarios = list(collection.find({}))

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="relatorio_usuarios.csv"'

    writer = csv.writer(response)
    writer.writerow(['userId', 'email', 'administrador', 'data cadastro', 'ativo', 'último login'])

    for usuario in usuarios:
        writer.writerow([usuario['id'], usuario['username'], usuario['is_staff'], usuario['date_joined'], usuario['is_active'], usuario['last_login']])       
    return response


@login_required(login_url='/login_user')
def models_listing(request):
    collection = dbname[getenv('COLLECTION_MODELS')]
    metricas = list(collection.find({}))
    return render(request, 'app/listing/models_listing.html', {'metricas':metricas})


@login_required(login_url='/login_user')
def generate_report_metrics(request):
    collection = dbname[getenv('COLLECTION_MODELS')]

    metricas = list(collection.find({}))

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="relatorio_metricas.csv"'

    writer = csv.writer(response)
    writer.writerow(['ModelID', 'Versão', 'Algoritmo', 'Acurácia', 'Recall', 'Precisão', 'Taxa de erro', 'F1', 'Logloss', 'AUC'])

    for metrica in metricas:
        writer.writerow([metrica['id'], metrica['version'], metrica['algorithm'], metrica['accuracy'], metrica['recall'], metrica['precision'], metrica['errorRate'], metrica['f1score'], metrica['logloss'], metrica['auc']])       
    return response


@login_required(login_url='/login_user')
def admin(request):
    return render(request, 'app/admin/admin.html')


@login_required(login_url='/login_user')
def profile(request):
    context = {'user': request.user}
    return render(request, 'app/profile/profile.html', context)


@login_required(login_url='/login_user')
def update_profile_form(request, user_id):
    user = User.objects.get(id=int(user_id))
    context = {'user': user}
    return render(request, 'app/profile/update_profile_form.html', context)


@login_required(login_url='/login_user')
def update_profile(request, user_id):
    if request.method == 'POST':
        user = User.objects.get(id=int(user_id))

        new_first_name = request.POST.get('first_name')
        new_last_name = request.POST.get('last_name')

        user.first_name = new_first_name
        user.last_name = new_last_name
        user.save()
        return redirect('app:profile')


@login_required(login_url='/login_user')
def about(request):
    if request.method == 'POST':
        title = request.POST.get('feedback_type')
        comment = request.POST.get('comment')

        user = request.user
        FeedbackUser.objects.create(title=title, comment=comment, username=user.username, name=user.get_full_name())
        return redirect('app:logged_user')
    return render(request, 'app/about/about.html')


@login_required(login_url='/login_user')
def feedbacks_listing(request):
    collection = dbname[getenv('COLLECTION_FEEDBACKS')]
    feedbacks = list(collection.find({}))
    return render(request, 'app/listing/feedbacks_listing.html', {'feedbacks':feedbacks})


@login_required(login_url='/login_user')
def generate_report_feedbacks(request):
    collection = dbname[getenv('COLLECTION_FEEDBACKS')]

    feedbacks = list(collection.find({}))

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="relatorio_feedbacks.csv"'

    writer = csv.writer(response)
    writer.writerow(['id', 'data', 'tipo', 'comentario', 'email', 'nome'])

    for feedback in feedbacks:
        writer.writerow([feedback['id'], feedback['date'], feedback['title'], feedback['comment'], feedback['username'], feedback['name']])       
    return response


@login_required(login_url='/login_user')
def create_ticket(request):
    user = request.user

    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        ticket = Ticket.objects.create(user=user, title=title, description=description, status='aberto')
        ticket.save()
        return redirect('app:ticket_list')
    return render(request, 'app/ticket/create_ticket.html')


@login_required(login_url='/login_user')
def ticket_list(request):
    collection = dbname[getenv('COLLECTION_TICKETS')]
    user = request.user

    if user.is_staff:
        tickets = list(collection.find())
    else:
        tickets = tickets = list(collection.find({'user_id': int(user.id)}))
    return render(request, 'app/ticket/ticket_list.html', {'tickets': tickets})


@login_required(login_url='/login_user')
def ticket_detail(request, ticket_id):
    user = request.user
    ticket = Ticket.objects.get(id=ticket_id)
    return render(request, 'app/ticket/ticket_detail.html', {'ticket': ticket})


@login_required(login_url='/login_user')
def generate_report_tickets(request):
    collection = dbname[getenv('COLLECTION_TICKETS')]
    user = request.user

    if user.is_staff:
        tickets = list(collection.find({}))
    else:
        tickets = list(collection.find({'user_id': int(user.id)}))

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="relatorio_tickets.csv"'

    writer = csv.writer(response)
    writer.writerow(['id', 'titulo', 'descricao', 'status', 'data criacao'])

    for ticket in tickets:
        writer.writerow([ticket['id'], ticket['title'], ticket['description'], ticket['status'], ticket['created_at']])       
    return response


@login_required(login_url='/login_user')
def ticket_complete(request, ticket_id):
    collection = dbname[getenv('COLLECTION_TICKETS')]
    collection.update_one({'id': int(ticket_id)}, {'$set': {'status': 'concluído'}})
    return redirect('app:ticket_list')


@login_required(login_url='/login_user')
def add_tips(request):
    if request.method == 'POST':
        title = request.POST['title']
        tip = request.POST['tip']
        responsible = request.POST['responsible']
        source= request.POST['source']
    
        tips = Tips.objects.create(title=title, tip=tip, responsible=responsible, source=source)
        tips.save()
        return redirect('app:add_tips')
    return render(request, 'app/education/insert_tips.html')


def chat(request):
    if request.method == 'POST':
        sender = request.POST['sender']
        email = request.POST['email']
        subject = request.POST['subject']
        message = request.POST['message']

        chat = Chat.objects.create(sender=sender, email=email, subject=subject, message=message)
        chat.save()

        assunto = f'No chat recebido: {subject}'
        email_sender_recipient = settings.EMAIL_HOST_USER
        email_message = f'Informações do chat:\nRemetente: {sender}\nEmail: {email}\nAssunto: {subject}\nMensagem: {message}'
        send_mail(assunto, email_message, email_sender_recipient, [email_sender_recipient], fail_silently=False)
        return redirect('app:index')
    return render(request, 'app/index.html')
