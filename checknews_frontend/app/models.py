import pymongo
from os import getenv
from django.db import models
from dotenv import load_dotenv
from django.utils import timezone
from django.contrib.auth.models import User

load_dotenv(verbose=True)

client = pymongo.MongoClient(getenv('URL_MONGO'))
dbname = client[getenv('DB_NAME')]
collection = dbname[getenv('COLLECTION')]


def get_current_date():
    return timezone.now()


class MetricsModel(models.Model):
    version = models.CharField(max_length=5)
    algorithm = models.TextField(max_length=50)
    accuracy = models.DecimalField(max_digits=3, decimal_places=3)
    recall = models.DecimalField(max_digits=3, decimal_places=3)
    precision = models.DecimalField(max_digits=3, decimal_places=3)
    errorRate = models.DecimalField(max_digits=3, decimal_places=3)
    f1score = models.DecimalField(max_digits=3, decimal_places=3)
    logloss = models.DecimalField(max_digits=3, decimal_places=3)
    auc = models.DecimalField(max_digits=3, decimal_places=3)

    def save(self, *args, **kwargs):
        report = {
            'version': self.version,
            'algorithm': self.algorithm,
            'accuracy': self.accuracy,
            'recall': self.recall,
            'precision': self.precision,
            'errorRate': self.errorRate,
            'f1score': self.f1score,
            'logloss': self.logloss,
            'auc': self.auc,
        }
        collection.insert_one(report)
        super(MetricsModel, self).save(*args, **kwargs)
    objects = models.Manager()


class FakeNewsDetection(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    link = models.TextField(max_length=500)
    content = models.TextField()
    classification = models.CharField(max_length=10)
    confidence = models.DecimalField(max_digits=10, decimal_places=5, default=1.0)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)


    def save(self, *args, **kwargs):
        report = {
            'date': self.date,
            'link': self.link,
            'content': self.content,
            'classification': self.classification,
            'confidence': float(self.confidence),
            'user_id': self.user_id
        }
        collection.insert_one(report)
        super(FakeNewsDetection, self).save(*args, **kwargs)
    objects = models.Manager()


class FakeNewsDetectionDetail(models.Model):
    news = models.ForeignKey(FakeNewsDetection, on_delete=models.CASCADE)
    date = models.DateTimeField(default=get_current_date)
    is_favorite = models.BooleanField(default=False)
    tags = models.CharField(max_length=100)
    review = models.IntegerField(default=0)
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        report = {
            'news_id': self.news.id,
            'date': self.date,
            'is_favorite': self.is_favorite,
            'tags': self.tags,
            'review': self.review
        }
        collection.insert_one(report)
        super(FakeNewsDetectionDetail, self).save(*args, **kwargs)
    objects = models.Manager()


class FeedbackUser(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    title = models.TextField(max_length=500)
    comment = models.TextField(help_text='Deixe o seu comentário')
    username = models.TextField(max_length=100, default='Não informado')
    name = models.TextField(max_length=500, default='Não informado')

    def save(self, *args, **kwargs):
        report = {
            'date': self.date,
            'title': self.title,
            'comment': self.comment,
            'username': self.username,
            'name': self.name
        }
        collection.insert_one(report)
        super(FeedbackUser, self).save(*args, **kwargs)
    objects = models.Manager()


class Ticket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    title = models.CharField(max_length=100)
    description = models.TextField(help_text='Relate o problema')
    status = models.CharField(max_length=20, default='aberto')
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        report = {
            'user_id': self.user_id,
            'title': self.title,
            'description': self.description,
            'status': self.status,
            'created_at': self.created_at
        }
        collection.insert_one(report)
        super(Ticket, self).save(*args, **kwargs)
    objects = models.Manager()


class Tips(models.Model):
    title = models.CharField(max_length=100)
    tip = models.TextField(help_text='Informe uma dica')
    date = models.DateTimeField(auto_now_add=True)
    responsible = models.TextField()
    source = models.TextField()

    def save(self, *args, **kwargs):
        report = {
            'title': self.title,
            'tip': self.tip,
            'date': self.date,
            'responsible': self.responsible,
            'source': self.source
        }
        collection.insert_one(report)
        super(Tips, self).save(*args, **kwargs)
    objects = models.Manager()


class Chat(models.Model):
    sender = models.CharField(max_length=100)
    subject = models.CharField(max_length=100)
    message = models.TextField()
    email = models.CharField(max_length=100, default=None)
    date = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        report = {
            'sender': self.sender,
            'subject': self.subject,
            'message': self.message,
            'email': self.email,
            'date': self.date
        }
        collection.insert_one(report)
        super(Chat, self).save(*args, **kwargs)
    objects = models.Manager()
