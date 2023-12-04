from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from .DataItem_model import DataItem


class DataEncryptionRequest(models.Model):
    class Status(models.TextChoices):
        # Черновик можно удалить или сформировать. Сформированную заявку можно завершить, отменить или удалить.
        DRAFT = "Черновик"
        FORMED = "Сформирован"
        FINALISED = "Завершён"
        CANCELLED = "Отменён"
        DELETED = "Удалён"

    work_status = models.TextField(choices=Status.choices, default=Status.DRAFT)
    creation_date = models.DateTimeField(default=timezone.now)
    formation_date = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    data_item = models.ManyToManyField(DataItem)
    
    class Action(models.IntegerChoices):
        ENCRYPT = 0
        DECRYPT = 1
    
    action = models.IntegerField(choices=Action.choices, default=Action.ENCRYPT)
    