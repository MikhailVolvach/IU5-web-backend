import os

from encryption.models import DataItem
from rest_framework import serializers
from django.conf import settings


class DataItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataItem
        fields = ["id", "img", "title", "file", "is_encrypted", "is_deleted", "data_type"]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        print(data)
        # Изменяем значение поля img
        if 'img' in data and data['img']:
            # Заменяем "http://nginx:9000" на "http://localhost:9000"
            data['img'] = data['img'].replace(os.environ.get('MINIO_HOST'), "http://localhost:9000")

        if 'file' in data and data['file']:
            data['file'] = data['file'].replace(os.environ.get('MINIO_HOST'), "http://localhost:9000")

        return data
