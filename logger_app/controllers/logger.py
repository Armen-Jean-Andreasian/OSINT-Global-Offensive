from service_response import ServiceResponse
from django.conf import settings
from logger_app.models import LoggerModel
from obtained_data_app.models import ObtainedDataModel
from user_app.models import UserModel
from typing import TYPE_CHECKING

REDIS_CACHE = settings.CACHE

if TYPE_CHECKING:
    from django.db.models.query import QuerySet


class LoggerController:
    @staticmethod
    def find_logger(logger_id) -> ServiceResponse:
        if not (logger_entry := REDIS_CACHE.get_instance(logger_id)):
            try:
                logger_entry: list = LoggerModel.objects.get(id=logger_id)
            except LoggerModel.DoesNotExist:
                return ServiceResponse(status=False, error="Logger not found")
        return ServiceResponse(status=True, data=logger_entry)


    @staticmethod
    def find_user_loggers(user_id) -> ServiceResponse:
        """
        Finds all loggers of a user with given id.
        First it looks for loggers in the cache by user_id, if not found, then looks in the database.
        """
        if not (loggers_entry := REDIS_CACHE.get_instance(user_id)):
            try:
                user = UserModel.objects.get(id=user_id)
                loggers: "QuerySet" = LoggerModel.objects.filter(user=user)
                loggers_entry = list(loggers)

                REDIS_CACHE.add_instance(instance_id=user_id, instance=loggers_entry)
                print("Logger found in DB.")
                return ServiceResponse(status=True, data=loggers_entry)

            except Exception as err:
                return ServiceResponse(status=False, error=str(err))
        else:
            print("Logger found in cache.")
            return ServiceResponse(status=True, data=loggers_entry)

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
        try:
            logger_entry = LoggerModel.objects.get(id=logger_id)
        except LoggerModel.DoesNotExist:
            return ServiceResponse(status=False, error="Logger not found")

        ObtainedDataModel.objects.filter(logger=logger_entry.data).delete()  # deleting "obtained data" entries
        logger_entry.data.delete()  # deleting the logger

        return ServiceResponse(status=True, message="Logger and its related obtained data successfully deleted.")
