from django.db import models
from django.utils import timezone

from django.contrib.auth.models import User

from app.models.DataItem_model import DataItem


class DataEncriptionRequest(models.Model):
    class Status(models.TextChoices):
        INTRODUCED = 'Введён'
        IN_WORK = "В работе"
        FINALISED = "Завершён"
        CANCELLED = "Отменён"
        DELETED = "Удалён"

    work_status = models.CharField(choices=Status.choices, default=Status.INTRODUCED)
    creation_date = models.DateTimeField(default=timezone.now)
    formation_date = models.DateTimeField()
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=1)
    
    data_item = models.ManyToManyField(DataItem)
    