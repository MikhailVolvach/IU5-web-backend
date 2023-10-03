from django.db import models
from django.utils import timezone
import datetime

class DataEncriptionRequest(models.Model):
    class Status(models.TextChoices):
        INTRODUCED = 'Введён'
        IN_WORK = "В работе"
        FINALISED = "Завершён"
        CANCELLED = "Отменён"
        DELETED = "Удалён"
    work_status = models.IntegerField(choices=Status.choices)
    creation_date = models.DateTimeField(default=timezone.now)
    formation_date = models.DateTimeField()
    