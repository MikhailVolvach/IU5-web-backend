from django.contrib import admin
from .models.DataItem_model import DataItem
from .models.DataEncryptionRequest_model import DataEncryptionRequest
from .models.EncryptionUser_model import EncryptionUser

class DataItemType(admin.ModelAdmin):
    list_display = ['title', 'is_deleted']

class EncryptionUserType(admin.ModelAdmin):
    list_display = ['username', 'is_staff']

admin.site.register(DataItem, DataItemType)
admin.site.register(DataEncryptionRequest)
admin.site.register(EncryptionUser)
