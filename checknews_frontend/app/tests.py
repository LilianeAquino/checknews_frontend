from django.test import TestCase
from django.core import mail
from django.contrib.auth.models import User
from app.models import MetricsModel, FakeNewsDetection, FeedbackUser, FakeNewsDetectionDetail, Ticket, Tips


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
