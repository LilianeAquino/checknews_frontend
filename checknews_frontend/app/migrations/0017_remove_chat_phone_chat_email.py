# Generated by Django 4.1.9 on 2023-06-18 12:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0016_chat'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='chat',
            name='phone',
        ),
        migrations.AddField(
            model_name='chat',
            name='email',
            field=models.CharField(default=None, max_length=100),
        ),
    ]