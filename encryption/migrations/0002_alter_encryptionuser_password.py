# Generated by Django 4.2.5 on 2023-11-29 06:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('encryption', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='encryptionuser',
            name='password',
            field=models.CharField(max_length=50, verbose_name='Пароль'),
        ),
    ]
