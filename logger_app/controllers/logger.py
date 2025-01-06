from service_response import ServiceResponse
from django.conf import settings
from logger_app.models import LoggerModel
from obtained_data_app.models import ObtainedDataModel
from user_app.models import UserModel
from typing import TYPE_CHECKING
from ..cache import LoggerCache

REDIS_CACHE = settings.CACHE

if TYPE_CHECKING:
    from django.db.models.query import QuerySet
    from uuid import UUID


class LoggerController:
    cache = LoggerCache

    @classmethod
    def find_logger(cls, logger_id: "UUID") -> ServiceResponse[bool, str] | ServiceResponse[bool, LoggerModel]:
        logger_from_redis: ServiceResponse = cls.cache.get_logger(logger_id)

        # if logger is not found in redis
        if not logger_from_redis:
            logger_from_db: LoggerModel = LoggerModel.objects.filter(id=logger_id).first()
            # if logger doesn't exist in db either
            if not logger_from_db:
                return ServiceResponse(status=False, error="Logger not found")

            # if logger exists in db
            cls.cache.set_logger(logger_id, logger_instance=logger_from_db)
            return ServiceResponse(status=True, data=logger_from_db)

        return ServiceResponse(status=True, data=logger_from_redis.data)

    @classmethod
    def find_user_loggers(cls, user_id: "UUID") -> ServiceResponse:
        """Retrieves all loggers of a user from cache or DB."""
        loggers_from_redis: ServiceResponse = cls.cache.get_loggers(user_id)

        # if logger is not found in redis
        if not loggers_from_redis:
            loggers_from_db: "QuerySet" = LoggerModel.objects.filter(user_id=user_id)
            loggers_from_db_list = list(loggers_from_db)
            # if loggers don't exist in db either
            if not loggers_from_db:
                return ServiceResponse(status=False, error="No loggers found for the user.")
            # if loggers exists in db
            cls.cache.set_loggers(user_id, logger_instances=loggers_from_db_list)
            return ServiceResponse(status=True, data=loggers_from_db_list)
        return ServiceResponse(status=True, data=loggers_from_redis.data)

    @classmethod
    def show(cls, logger_id: "UUID"):
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
    def delete(cls, logger_id: "UUID"):
        try:
            logger_entry = LoggerModel.objects.get(id=logger_id)
        except LoggerModel.DoesNotExist:
            return ServiceResponse(status=False, error="Logger not found")

        ObtainedDataModel.objects.filter(logger=logger_entry.data).delete()  # deleting "obtained data" entries
        logger_entry.data.delete()  # deleting the logger
        cls.cache.delete_logger(logger_id) # deleting the logger from cache

        return ServiceResponse(status=True, message="Logger and its related obtained data successfully deleted.")
