# Generated by Django 4.2.5 on 2023-11-29 06:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('encryption', '0003_alter_encryptionuser_password'),
    ]

    operations = [
        migrations.AlterField(
            model_name='encryptionuser',
            name='password',
            field=models.CharField(max_length=128, verbose_name='password'),
        ),
    ]
