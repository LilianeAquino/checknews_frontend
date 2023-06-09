# Generated by Django 4.1.9 on 2023-06-08 13:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_alter_fakenewsdetection_confidence'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fakenewsdetection',
            name='confidence',
            field=models.DecimalField(decimal_places=5, default=1.0, max_digits=10),
        ),
        migrations.CreateModel(
            name='FakeNewsDetectionDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_favorite', models.BooleanField(default=False)),
                ('tags', models.CharField(max_length=100)),
                ('news', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.fakenewsdetection')),
            ],
        ),
    ]
