from django.contrib import admin
from .models.DataItem_model import DataItem
from .models.DataEncryptionRequest_model import DataEncryptionRequest

class DataItemType(admin.ModelAdmin):
    list_display= ['title', 'is_deleted']

admin.site.register(DataItem, DataItemType)
admin.site.register(DataEncryptionRequest)
