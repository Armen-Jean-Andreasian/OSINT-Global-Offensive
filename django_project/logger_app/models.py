from django.db import models
import uuid
import os


class LoggerModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey('user_app.UserModel', on_delete=models.CASCADE)
    destination = models.CharField(max_length=255, blank=False, null=False)
    fake_url = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        """Override the save method to automatically generate the fake_url before saving the object."""
        if not self.fake_url:
            # TODO
            self.fake_url = 'http://' + os.environ.get('DOMAIN_FOR_FAKE_URL') + f":80" + f"/obtain_data/{self.id}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Logger for {self.user} - {self.destination}"

    class Meta:
        verbose_name = "Logger"
        verbose_name_plural = "Loggers"
