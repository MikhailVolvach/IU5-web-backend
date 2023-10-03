from django.db import models

class User(models.Model):
    name = models.CharField(max_length=30)
    is_moderator = models.BooleanField()