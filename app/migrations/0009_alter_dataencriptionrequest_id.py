# Generated by Django 4.2.5 on 2023-10-03 19:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_dataitem_data_encription_request'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dataencriptionrequest',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
