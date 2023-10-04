from django.contrib import admin
from .models.User_model import User
from .models.DataItem_model import DataItem
from .models.DataEncriptionRequest_model import DataEncriptionRequest

class DataItemType(admin.ModelAdmin):
    list_display= ['title', 'is_deleted']

admin.site.register(User)
admin.site.register(DataItem, DataItemType)
admin.site.register(DataEncriptionRequest)


