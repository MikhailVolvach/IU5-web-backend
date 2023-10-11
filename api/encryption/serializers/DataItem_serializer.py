from encryption.models import DataItem
from rest_framework import serializers

class DataItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataItem
        fields = ["id", "img", "title", "file", "is_encripted", "is_deleted", "data_type"]