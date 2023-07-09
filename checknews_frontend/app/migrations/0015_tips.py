# Generated by Django 4.1.9 on 2023-06-14 22:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0014_ticket'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tips',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('tip', models.TextField(help_text='Relate o problema')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('responsible', models.TextField()),
                ('source', models.TextField()),
            ],
        ),
    ]
