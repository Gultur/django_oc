# Generated by Django 2.1.2 on 2018-10-12 07:48

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MiniUrl',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url_longue', models.URLField(unique=True)),
                ('code', models.CharField(max_length=20, unique=True)),
                ('date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Date de génération')),
                ('pseudo', models.CharField(max_length=20)),
                ('nombre_acces', models.IntegerField(default=0)),
            ],
        ),
    ]
