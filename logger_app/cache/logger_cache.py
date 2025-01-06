from django.core.cache import cache
from abstractions.model_cache_abs import AbsModelCache
from service_response import ServiceResponse
from typing import TYPE_CHECKING
from ..models import LoggerModel

if TYPE_CHECKING:
    from uuid import UUID


class LoggerCache(AbsModelCache):
    SINGLE_ITEM_KEY_TEMPLATE = "logger:{logger_id}"
    MULTIPLE_ITEMS_KEY_TEMPLATE = "loggers:user:{user_id}"
    TTL: int

    @classmethod
    def get_logger(cls, logger_id: "UUID") -> ServiceResponse[bool, str] | ServiceResponse[bool, LoggerModel]:
        """Retrieve a single logger from cache or DB."""
        cache_key = cls.SINGLE_ITEM_KEY_TEMPLATE.format(logger_id=logger_id)
        if logger_from_redis := cache.get(cache_key):  # Logger
            return ServiceResponse(status=True, data=logger_from_redis)
        return ServiceResponse(status=False, data=None)

    @classmethod
    def set_logger(cls, logger_id: "UUID", logger_instance: LoggerModel) -> None:
        """Cache a single logger."""
        cache_key = cls.SINGLE_ITEM_KEY_TEMPLATE.format(logger_id=logger_id)
        cache.set(cache_key, logger_instance, cls.TTL)

    @classmethod
    def get_loggers(cls, user_id: "UUID") -> ServiceResponse[bool, str] | ServiceResponse[bool, list[LoggerModel]]:
        """Retrieves all loggers of a user from cache or DB."""
        cache_key = cls.MULTIPLE_ITEMS_KEY_TEMPLATE.format(user_id=user_id)
        if loggers_from_redis := cache.get(cache_key):  # list
            return ServiceResponse(status=True, data=loggers_from_redis)
        return ServiceResponse(status=False, data=None)

    @classmethod
    def set_loggers(cls, user_id: "UUID", logger_instances: list[LoggerModel]) -> None:
        """Cache multiple loggers for a user."""
        cache_key = cls.MULTIPLE_ITEMS_KEY_TEMPLATE.format(user_id=user_id)
        cache.set(cache_key, logger_instances, cls.TTL)

    @classmethod
    def delete_logger(cls, logger_id: "UUID") -> ServiceResponse[bool, str]:
        """Delete a single logger from cache."""
        cache_key = cls.SINGLE_ITEM_KEY_TEMPLATE.format(logger_id=logger_id)

        if cache.delete(cache_key):
            return ServiceResponse(status=True, message=f"Logger with ID {logger_id} deleted from cache.")
        return ServiceResponse(status=False, message=f"Logger with ID {logger_id} not found in cache.")

    @classmethod
    def delete_loggers(cls, user_id: "UUID"):
        """Delete all loggers for a user from cache."""
        cache_key = cls.MULTIPLE_ITEMS_KEY_TEMPLATE.format(user_id=user_id)

        if cache.delete(cache_key):
            return ServiceResponse(status=True, message=f"All loggers for user {user_id} deleted from cache.")
        return ServiceResponse(status=False, message=f"No loggers found for user {user_id} in cache.")
