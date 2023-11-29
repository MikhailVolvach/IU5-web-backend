from rest_framework import serializers
from encryption.models import EncryptionUser

class EncryptionUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = EncryptionUser
        fields = ['username', 'password', 'role']