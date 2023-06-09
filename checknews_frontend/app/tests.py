from django.contrib.auth.models import User
from django.test import TestCase, Client
from dotenv import load_dotenv
from django.urls import reverse
from unittest.mock import patch
from django.core import mail
from os import getenv
import pymongo
import csv
from io import StringIO

from app.forms import UserRegisterForm
from app.models import MetricsModel, FakeNewsDetection, FeedbackUser, FakeNewsDetectionDetail, Ticket, Tips, Chat

load_dotenv(verbose=True)


client = pymongo.MongoClient(getenv('URL_MONGO'))
dbname = client[getenv('DB_NAME')]


class ModelTestCase(TestCase):

    def setUp(self):
        self.metrics_model = MetricsModel.objects.create(
            version='v1.0',
            algorithm='LinearSVC',
            accuracy=0.918,
            recall=0.918,
            precision=0.92,
            errorRate=0.15,
            f1score=0.918,
            logloss=0.194,
            auc=0.918,
        )

        self.fake_news_detection = FakeNewsDetection.objects.create(
            link='https://example.com',
            content='Fake news content',
            classification='Fake',
            confidence=0.951,
            user_id=1
        )

        self.feedback_user = FeedbackUser.objects.create(
            title='Feedback Title',
            comment='Feedback comment',
            username='lilane@email',
            name='Liliane'
        )
        
        self.fake_news_detection_detail = FakeNewsDetectionDetail(
            news = self.fake_news_detection,
            is_favorite = True,
            tags = '#true',
            review = 5
        )

        self.user = User.objects.create(username='testuser')
        self.ticket = Ticket(
            user = self.user,
            title = 'title',
            description = 'description',
            status = 'aberto'
        )

        self.tips = Tips.objects.create(
            title = 'title',
            tip = 'tip',
            responsible = 'Liliane',
            source = 'http//link'
        )

        self.chat = Chat.objects.create(
            sender = 'Liliane',
            subject = 'Conversa',
            message = 'Essa é uma mensagem',
            email = 'lilane@email'
        )


    def test_metrics_model(self):
        self.assertEqual(self.metrics_model.version, 'v1.0')
        self.assertEqual(self.metrics_model.algorithm, 'LinearSVC')
        self.assertEqual(round(float(self.metrics_model.accuracy), 3), 0.918)
        self.assertEqual(round(float(self.metrics_model.recall), 3), 0.918)
        self.assertEqual(round(float(self.metrics_model.precision), 3), 0.92)
        self.assertEqual(round(float(self.metrics_model.errorRate), 3), 0.15)
        self.assertEqual(round(float(self.metrics_model.f1score), 3), 0.918)
        self.assertEqual(round(float(self.metrics_model.auc), 3), 0.918)
        self.assertEqual(round(float(self.metrics_model.logloss), 3), 0.194)


    def test_fake_news_detection(self):
        self.assertEqual(self.fake_news_detection.link, 'https://example.com')
        self.assertEqual(self.fake_news_detection.content, 'Fake news content')
        self.assertEqual(self.fake_news_detection.classification, 'Fake')
        self.assertEqual(round(float(self.fake_news_detection.confidence), 3), 0.951)
        self.assertEqual(self.fake_news_detection.user_id, 1)


    def test_fake_news_detection_detail(self):
        self.assertEqual(self.fake_news_detection_detail.news, self.fake_news_detection)
        self.assertEqual(self.fake_news_detection_detail.is_favorite, True)
        self.assertEqual(self.fake_news_detection_detail.tags, '#true')
        self.assertEqual(self.fake_news_detection_detail.review, 5)


    def test_feedback_user(self):
        self.assertEqual(self.feedback_user.title, 'Feedback Title')
        self.assertEqual(self.feedback_user.comment, 'Feedback comment')
        self.assertEqual(self.feedback_user.username, 'lilane@email')
        self.assertEqual(self.feedback_user.name, 'Liliane')


    def test_ticket(self):
        self.assertEqual(self.ticket.user, self.user)
        self.assertEqual(self.ticket.title, 'title')
        self.assertEqual(self.ticket.description, 'description')
        self.assertEqual(self.ticket.status, 'aberto')


    def test_tips(self):
        self.assertEqual(self.tips.title, 'title')
        self.assertEqual(self.tips.tip, 'tip')
        self.assertEqual(self.tips.responsible, 'Liliane')
        self.assertEqual(self.tips.source, 'http//link')


    def test_chat(self):
        self.assertEqual(self.chat.sender, 'Liliane')
        self.assertEqual(self.chat.subject, 'Conversa')
        self.assertEqual(self.chat.message, 'Essa é uma mensagem')
        self.assertEqual(self.chat.email, 'lilane@email')

class EmailTestCase(TestCase):
    def test_send_email(self):
        mail.send_mail(
            'Assunto', 'Corpo da mensagem',
            'from@yourdjangoapp.com', ['to@yourbestuser.com'],
            fail_silently=False,
        )

        self.assertEqual(len(mail.outbox), 1)        
        self.assertEqual(mail.outbox[0].subject, 'Assunto')
        self.assertEqual(mail.outbox[0].body, 'Corpo da mensagem')


class UserRegisterFormTest(TestCase):
    def test_form_valid_data(self):
        form_data = {
            'email': 'example@example.com',
            'senha': 'password',
        }
        form = UserRegisterForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_missing_data(self):
        form_data = {
            'email': '',
            'senha': 'password',
        }
        form = UserRegisterForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['email'], ['Este campo é obrigatório.'])

    def test_form_invalid_email(self):
        form_data = {
            'email': 'email_invalido',
            'senha': 'password',
        }
        form = UserRegisterForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['email'], ['Informe um endereço de email válido.'])


class DeleteUserViewTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_delete_user(self):
        user_id = 1
        collection = dbname[getenv('COLLECTION_USERS')]
        collection.insert_one({'id': user_id})

        response = self.client.post(reverse('app:delete_user', args=[user_id]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('app:users_listing'), fetch_redirect_response=False)

        user_exists = collection.find_one({'id': user_id})
        self.assertIsNone(user_exists)


class UpdateUserViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword', is_staff=True)

    def test_update_user(self):
        user_id = self.user.id
        username = 'newusername'
        first_name = 'New'
        last_name = 'User'
        is_staff = False
        is_active = False

        response = self.client.post(reverse('app:update_user', args=[user_id]), {
            'username': username,
            'first_name': first_name,
            'last_name': last_name,
            'is_staff': is_staff,
            'is_active': is_active,
        })

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('app:users_listing'), fetch_redirect_response=False)

        updated_user = User.objects.get(id=user_id)
        self.assertEqual(updated_user.username, username)
        self.assertEqual(updated_user.first_name, first_name)
        self.assertEqual(updated_user.last_name, last_name)
        self.assertEqual(updated_user.is_staff, is_staff)
        self.assertEqual(updated_user.is_active, is_active)


class CreateUserViewTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_create_user(self):
        username = 'newuser'
        first_name = 'New'
        last_name = 'User'
        password = 'testpassword'
        is_staff = False

        response = self.client.post(reverse('app:create_user'), {
            'username': username,
            'first_name': first_name,
            'last_name': last_name,
            'password': password,
            'is_staff': is_staff,
        })

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('app:users_listing'), fetch_redirect_response=False)

        created_user = User.objects.get(username=username)
        self.assertEqual(created_user.username, username)
        self.assertEqual(created_user.first_name, first_name)
        self.assertEqual(created_user.last_name, last_name)
        self.assertTrue(created_user.check_password(password))
        self.assertEqual(created_user.is_staff, is_staff)


class ProcessFormNewsViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    @patch('requests.get')
    @patch('requests.post')
    def test_process_form_news(self, mock_post, mock_get):
        link = 'https://example.com'
        text = 'Example news content'
        classification = 'Fake'
        confidence = float(0.8)

        mock_post.return_value.json.return_value = {
            'classification': {'label': classification, 'confianca': confidence}
        }

        mock_get.return_value.content = text.encode('utf-8')
        self.client.login(username='testuser', password='testpassword')

        response = self.client.post(reverse('app:process_form_news'), {
            'url': link,
        })

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('app:checked_news'), fetch_redirect_response=False)

        result_check = FakeNewsDetection.objects.first()
        self.assertEqual(result_check.link, link)
        self.assertEqual(result_check.content, text)
        self.assertEqual(result_check.classification, classification)
        self.assertEqual(float(result_check.confidence.to_decimal()), confidence)
        self.assertEqual(result_check.user_id, self.user.id)

        mock_get.assert_called_once_with(link)
        mock_post.assert_called_once()

    def test_process_form_news_not_authenticated(self):
        response = self.client.post(reverse('app:process_form_news'), {'url': 'https://example.com'}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app/login/login.html')
