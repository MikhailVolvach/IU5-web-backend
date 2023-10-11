from django.db import models

class DataItem(models.Model):
    img = models.ImageField(upload_to="images", blank=True)
    title = models.CharField(max_length=50)
    file = models.FileField(upload_to="data", blank=True)
    
    def get_file_name(self):
        if self.file:
            return self.file.name
        return ""
    
    class IsEncrypted(models.IntegerChoices):
        ENCRYPTED = 1
        ORIGINAL = 2
    
    is_encrypted = models.IntegerField(choices=IsEncrypted.choices, default=IsEncrypted.ORIGINAL)
    
    is_deleted = models.BooleanField(default=False)
    
    class DataType(models.IntegerChoices):
        TEXT_FILE = 1
        CODE = 2
        IMAGE = 3
        
    data_type = models.IntegerField(choices=DataType.choices, default=DataType.TEXT_FILE)

    def set_is_deleted(self):
        self.is_deleted = True
    
    