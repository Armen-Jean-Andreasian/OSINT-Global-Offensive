from django.db import models
from datetime import datetime


class ObtainedDataModel(models.Model):
    """Doesn't have separate id."""
    logger = models.ForeignKey('logger_app.LoggerModel', on_delete=models.CASCADE, related_name='obtained_datas')
    date_time = models.DateTimeField(default=datetime.utcnow)
    ip = models.CharField(max_length=45, db_index=True)
    browser = models.CharField(max_length=100, blank=True, null=True)
    operating_system = models.CharField(max_length=100, blank=True, null=True)
    user_agent = models.CharField(max_length=255, blank=True, null=True)
    host_name = models.CharField(max_length=255, blank=True, null=True)  # DNS name
    isp = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"ObtainedDataModel from {self.ip} at {self.date_time}"
