from django.contrib import admin
from .models import Equipment, DatasetUpload


@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    list_display = ['equipment_name', 'type', 'flowrate', 'pressure', 'temperature', 'dataset', 'created_at']
    list_filter = ['type', 'dataset', 'created_at']
    search_fields = ['equipment_name', 'type']
    ordering = ['-created_at']
    readonly_fields = ['created_at']


@admin.register(DatasetUpload)
class DatasetUploadAdmin(admin.ModelAdmin):
    list_display = ['filename', 'upload_timestamp', 'total_count', 'avg_flowrate', 'avg_pressure', 'avg_temperature']
    list_filter = ['upload_timestamp']
    search_fields = ['filename']
    ordering = ['-upload_timestamp']
    readonly_fields = ['upload_timestamp', 'total_count', 'avg_flowrate', 'avg_pressure', 'avg_temperature', 'type_distribution']
