# Generated by Django 4.1.9 on 2023-06-07 22:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_fakenewsdetection_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fakenewsdetection',
            name='confidence',
            field=models.DecimalField(decimal_places=3, default=1.0, max_digits=3),
        ),
    ]
