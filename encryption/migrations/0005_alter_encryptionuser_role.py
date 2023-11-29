# Generated by Django 4.2.5 on 2023-11-24 12:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('encryption', '0004_remove_encryptionpermission_permission_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='encryptionuser',
            name='role',
            field=models.IntegerField(blank=True, choices=[(1, 'User'), (2, 'Moderator'), (3, 'Admin')], default=1, verbose_name='Роль пользователя'),
        ),
    ]
