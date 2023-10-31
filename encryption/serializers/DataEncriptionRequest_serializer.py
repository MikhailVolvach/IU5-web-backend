from encryption.models import DataEncryptionRequest
from rest_framework import serializers

class DataEncriptionRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataEncryptionRequest
        fields = ["id", "work_status", "creation_date", "formation_date", "user_id", "action"]