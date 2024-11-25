from django.db import models


class LoggerModel(models.Model):
    user = models.ForeignKey('user_app.UserModel', on_delete=models.CASCADE)
    original_url = models.CharField(max_length=255, blank=False, null=False)
    fake_url = models.CharField(max_length=255, blank=False, null=False)
