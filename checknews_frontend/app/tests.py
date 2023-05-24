from django.test import TestCase
from django.core import mail
from django.contrib.auth.models import User
from app.models import MetricsModel, FakeNewsDetection, FeedbackUser, UserAccount


class ModelTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='userTest', password='passwordTest')
        self.account = UserAccount.objects.create(user=self.user, isAdministrator=True)

        self.metrics_model = MetricsModel.objects.create(
            version='v1.0',
            model='classifier_model.sav',
            algoritm='LinearSVC',
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
            confidence=0.951
        )
        self.feedback_user = FeedbackUser.objects.create(
            title='Feedback Title',
            comment='Feedback comment'
        )


    def test_user_account(self):
        self.assertEqual(str(self.account), 'userTest')
        self.assertTrue(self.account.isAdministrator)
        self.assertIsNotNone(self.account.dateCreated)


    def test_metrics_model(self):
        self.assertEqual(self.metrics_model.version, 'v1.0')
        self.assertEqual(self.metrics_model.model, 'classifier_model.sav')
        self.assertEqual(self.metrics_model.algoritm, 'LinearSVC')
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


    def test_feedback_user(self):
        self.assertEqual(self.feedback_user.title, 'Feedback Title')
        self.assertEqual(self.feedback_user.comment, 'Feedback comment')


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