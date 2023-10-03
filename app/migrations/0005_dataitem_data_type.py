# Generated by Django 4.2.5 on 2023-10-03 18:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_alter_dataencriptionrequest_creation_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='dataitem',
            name='data_type',
            field=models.CharField(choices=[('Текстовый файл', 'Text File'), ('Код', 'Code'), ('Изображение', 'Image')], default='Текстовый файл'),
        ),
    ]
