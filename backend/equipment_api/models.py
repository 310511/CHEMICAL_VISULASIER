from django.db import models
from django.utils import timezone


class DatasetUpload(models.Model):
    filename = models.CharField(max_length=255)
    upload_timestamp = models.DateTimeField(auto_now_add=True)
    total_count = models.IntegerField()
    avg_flowrate = models.FloatField()
    avg_pressure = models.FloatField()
    avg_temperature = models.FloatField()
    type_distribution = models.JSONField(default=dict)

    class Meta:
        ordering = ['-upload_timestamp']

    def __str__(self):
        return f"{self.filename} ({self.upload_timestamp.strftime('%Y-%m-%d %H:%M')})"


class Equipment(models.Model):
    EQUIPMENT_TYPES = [
        ('Reactor', 'Reactor'),
        ('Pump', 'Pump'),
        ('Heat Exchanger', 'Heat Exchanger'),
        ('HeatExchanger', 'Heat Exchanger'),
        ('Compressor', 'Compressor'),
        ('Valve', 'Valve'),
        ('Condenser', 'Condenser'),
    ]

    equipment_name = models.CharField(max_length=200)
    type = models.CharField(max_length=100, choices=EQUIPMENT_TYPES)
    flowrate = models.FloatField()
    pressure = models.FloatField()
    temperature = models.FloatField()
    dataset = models.ForeignKey(DatasetUpload, on_delete=models.CASCADE, related_name='equipment')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.equipment_name} - {self.type}"
