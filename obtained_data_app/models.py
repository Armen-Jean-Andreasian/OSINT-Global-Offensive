from django.db import models
from datetime import datetime
from components import ServiceResponse


class ObtainedDataModel(models.Model):
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

    @classmethod
    def index(cls, logger_id: int) -> ServiceResponse:
        """Returns all obtained data objects of a logger with the given logger id."""
        data = list(cls.objects.filter(logger__id=logger_id))
        if data:
            return ServiceResponse(status=True, data=data)
        else:
            return ServiceResponse(status=False, data=data, message="No obtained data found.")

    @classmethod
    def destroy(cls, logger_id: int) -> ServiceResponse:
        """Deletes all obtained data objects of a logger with the given logger id."""
        found_data_resp: ServiceResponse = cls.index(logger_id)

        if not found_data_resp:
            return found_data_resp
        else:
            removed_data_count: int = 0
            try:
                for data in found_data_resp.data:
                    data.delete()
                    removed_data_count += 1
            except Exception as err:
                return ServiceResponse(
                    status=False,
                    message=f"Failed to delete remaining records. {removed_data_count} data records deleted.",
                    error=str(err)
                )
            else:
                return ServiceResponse(status=True, message=f"{removed_data_count} data records deleted.")
