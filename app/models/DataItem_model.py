import os

from django.db import models

class DataItem(models.Model):
    img = models.ImageField(upload_to="images")
    title = models.CharField(max_length=50)
    file = models.FileField(upload_to="data")
    
    def getFileName(self):
        return self.file.name
    
    class IsEncripted(models.TextChoices):
        ENCRYPTED = "Зашифровано"
        ORIGINAL = "Оригинал"
    
    encription_status = models.CharField(choices=IsEncripted.choices)
    
    # class Status(models.TextChoices):
    #     DELETED = "Удалён"
    #     IN_EFFECT = "Действует"
    
    is_deleted = models.BooleanField(default=False)
    
    class DataType(models.TextChoices):
        TEXT_FILE = "Текстовый файл"
        CODE = "Код"
        IMAGE = "Изображение"
        # DIRECTORY = "Директория"
        
    data_type = models.CharField(choices=DataType.choices, default=DataType.TEXT_FILE)
    
    