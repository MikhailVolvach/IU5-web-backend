# Generated by Django 4.2.5 on 2023-10-11 11:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('encryption', '0002_alter_dataencryptionrequest_work_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dataencryptionrequest',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
