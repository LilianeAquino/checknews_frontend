# Generated by Django 4.1.9 on 2023-07-06 22:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0017_remove_chat_phone_chat_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tips',
            name='tip',
            field=models.TextField(help_text='Informe uma dica'),
        ),
    ]