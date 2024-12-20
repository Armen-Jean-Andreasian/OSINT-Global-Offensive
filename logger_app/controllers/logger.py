from logger_app.models import LoggerModel
from obtained_data_app.models import ObtainedDataModel
from components import ServiceResponse
from user_app.models import UserModel
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from django.db.models.query import QuerySet


class LoggerController:
    @staticmethod
    def find_logger(logger_id) -> ServiceResponse:
        try:
            logger_entry = LoggerModel.objects.get(id=logger_id)
            print("logger_entry", type(logger_entry))
        except LoggerModel.DoesNotExist:
            return ServiceResponse(status=False, error="Logger not found")
        else:
            print("logger_entry", type(logger_entry))
            return ServiceResponse(status=True, data=logger_entry)

    @staticmethod
    def find_user_loggers(user_id) -> ServiceResponse:
        try:
            user = UserModel.objects.get(id=user_id)
            loggers: "QuerySet" = LoggerModel.objects.filter(user=user)
        except Exception as err:
            return ServiceResponse(status=False, error=str(err))
        else:
            return ServiceResponse(status=True, data=list(loggers))

    @classmethod
    def show(cls, logger_id):
        """Returns the logger object of a user with given id."""
        return cls.find_logger(logger_id)

    @classmethod
    def create(cls, destination: str, user_id: int) -> LoggerModel:
        """
        Creates a new logger for a user.

        :param destination: The destination URL to be logged
        :param user_id: The id of the user to create the logger for
        """

        user = UserModel.objects.get(id=user_id)
        new_logger = LoggerModel(user=user, destination=destination)
        new_logger.save()
        return new_logger

    @classmethod
    def delete(cls, logger_id):
        if logger_entry := cls.find_logger(logger_id):

            ObtainedDataModel.objects.filter(logger=logger_entry.data).delete()  # deleting "obtained data" entries
            logger_entry.data.delete()  # deleting the logger

            return ServiceResponse(status=True, message="Logger and its related obtained data successfully deleted.")
        else:
            return ServiceResponse(status=False, error=logger_entry.error)
