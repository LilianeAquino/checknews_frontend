# Generated by Django 4.2 on 2023-04-27 21:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feedbackuser',
            name='comment',
            field=models.TextField(help_text='Deixe o seu comentário'),
        ),
    ]
