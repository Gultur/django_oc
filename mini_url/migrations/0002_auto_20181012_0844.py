# Generated by Django 2.1.2 on 2018-10-12 08:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mini_url', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='miniurl',
            name='code',
            field=models.CharField(max_length=6, unique=True),
        ),
    ]
