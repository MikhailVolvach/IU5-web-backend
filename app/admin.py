from django.contrib import admin
from .models.User_model import User
from .models.DataItem_model import DataItem
from .models.DataEncriptionRequest_model import DataEncriptionRequest

admin.site.register(User)
admin.site.register(DataItem)
admin.site.register(DataEncriptionRequest)
