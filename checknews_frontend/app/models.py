from django.db import models
from django.contrib.auth.models import User
import pymongo


client = pymongo.MongoClient('localhost:27017')
dbname = client['checknewsDB']
collection = dbname['checknews']


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
    confidence = models.DecimalField(max_digits=3, decimal_places=3)

    def save(self, *args, **kwargs):
        report = {
            'date': self.date,
            'link': self.link,
            'content': self.content,
            'classification': self.classification,
            'confidence': self.confidence
        }
        collection.insert_one(report)
        super(FakeNewsDetection, self).save(*args, **kwargs)
    objects = models.Manager()


class FeedbackUser(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    title = models.TextField(max_length=500)
    comment = models.TextField(help_text='Deixe o seu comentário')


    def save(self, *args, **kwargs):
        report = {
            'date': self.date,
            'title': self.title,
            'comment': self.comment
        }
        collection.insert_one(report)
        super(FeedbackUser, self).save(*args, **kwargs)
    objects = models.Manager()
