from rest_framework import serializers
from .models import Equipment, DatasetUpload


class EquipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Equipment
        fields = ['id', 'equipment_name', 'type', 'flowrate', 'pressure', 'temperature']


class DatasetUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = DatasetUpload
        fields = ['id', 'filename', 'upload_timestamp', 'total_count', 'avg_flowrate', 
                 'avg_pressure', 'avg_temperature', 'type_distribution']


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class LogoutSerializer(serializers.Serializer):
    pass


class FileUploadSerializer(serializers.Serializer):
    file = serializers.FileField()
