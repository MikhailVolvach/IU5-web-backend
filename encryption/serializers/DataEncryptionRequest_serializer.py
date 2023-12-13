from encryption.models import DataEncryptionRequest
from rest_framework import serializers
from django.contrib.auth.models import User

class DataEncryptionRequestSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    class Meta:        
        model = DataEncryptionRequest
        fields = ["id", "work_status", "creation_date", "formation_date", "user", "action"]
    
    def get_user(self, obj):
        return obj.user.username if obj.user else None