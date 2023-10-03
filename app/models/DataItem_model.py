from django.db import models
from app.models.DataEncriptionRequest_model import DataEncriptionRequest

class DataItem(models.Model):
    img = models.ImageField(upload_to="images")
    title = models.CharField(max_length=50)
    file = models.FileField(upload_to="data")
    
    class IsEncripted(models.TextChoices):
        ENCRYPTED = "Зашифровано"
        ORIGINAL = "Оригинал"
    
    encription_status = models.CharField(choices=IsEncripted.choices)
    
    class Status(models.TextChoices):
        DELETED = "Удалён"
        IN_EFFECT = "Действует"
    
    status = models.CharField(choices=Status.choices, default=Status.IN_EFFECT)
    
    class DataType(models.TextChoices):
        TEXT_FILE = "Текстовый файл"
        CODE = "Код"
        IMAGE = "Изображение"
        # DIRECTORY = "Директория"
        
    data_type = models.CharField(choices=DataType.choices, default=DataType.TEXT_FILE)
    
    data_encription_request = models.ManyToManyField(DataEncriptionRequest)
    
    