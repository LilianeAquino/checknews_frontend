# Generated by Django 4.1.9 on 2023-06-01 21:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_remove_metricsmodel_model'),
    ]

    operations = [
        migrations.RenameField(
            model_name='metricsmodel',
            old_name='algoritm',
            new_name='algorithm',
        ),
    ]