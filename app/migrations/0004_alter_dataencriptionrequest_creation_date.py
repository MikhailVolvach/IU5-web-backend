# Generated by Django 4.2.5 on 2023-09-28 14:51

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_alter_dataencriptionrequest_creation_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dataencriptionrequest',
            name='creation_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]