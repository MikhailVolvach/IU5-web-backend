# Generated by Django 4.2.5 on 2023-10-04 11:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app', '0012_remove_dataitem_status_dataitem_is_deleted'),
    ]

    operations = [
        migrations.AddField(
            model_name='dataencriptionrequest',
            name='user_id',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]