from django.db import models
from django.utils import timezone

from django.contrib.auth.models import User

from .DataItem_model import DataItem


class DataEncryptionRequest(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'Черновик'
        FORMED = "Сформирован"
        FINALISED = "Завершён"
        CANCELLED = "Отменён"
        DELETED = "Удалён"

    work_status = models.TextField(choices=Status.choices, default=Status.DRAFT)
    creation_date = models.DateTimeField(default=timezone.now)
    formation_date = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    
    data_item = models.ManyToManyField(DataItem)

    def set_is_deleted(self):
        self.work_status = self.Status.DELETED
    