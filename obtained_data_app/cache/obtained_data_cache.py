from django.core.cache import cache
from abstractions.model_cache_abs import AbsModelCache
from service_response import ServiceResponse
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from uuid import UUID
    from ..models import ObtainedDataModel


class ObtainedDataCache(AbsModelCache):
    """
    As ObtainedData is just a part of one-to many relation, they don't need to have id.
    And they are being retrieved using the id of a logger they belong to.
    """

    MULTIPLE_ITEMS_KEY_TEMPLATE = "obtained_data:logger:{logger_id}"
    TTL: int

    @classmethod
    def get_obtained_datum(cls, logger_id: "UUID") -> ServiceResponse[bool, str] | ServiceResponse[bool, "ObtainedDataModel"]:
        """Retrieves obtained datum of a logger from cache."""
        cache_key = cls.MULTIPLE_ITEMS_KEY_TEMPLATE.format(logger_id=logger_id)

        if obtained_datum_from_redis := cache.get(cache_key):  # list
            return ServiceResponse(status=True, data=obtained_datum_from_redis)
        return ServiceResponse(status=False, data=None)

    @classmethod
    def set_obtained_datum(cls, logger_id: "UUID", obtained_data_instances: list["ObtainedDataModel"]) -> None:
        """
        Cache multiple obtained datum for a logger.

        :return None: As redis is integrated into Django no situations may appear when Redis stopped or crashed,
            however the Django server keeps functioning as normal.
        """
        cache_key = cls.MULTIPLE_ITEMS_KEY_TEMPLATE.format(logger_id=logger_id)
        cache.set(cache_key, obtained_data_instances, cls.TTL)

    @classmethod
    def delete_obtained_datum(cls, logger_id: "UUID") -> ServiceResponse[bool, str]:
        """Delete all obtained datum for a logger from cache."""
        cache_key = cls.MULTIPLE_ITEMS_KEY_TEMPLATE.format(logger_id=logger_id)
        if cache.delete(cache_key):
            return ServiceResponse(status=True, message=f"Obtained datum belong to Logger with ID {logger_id} deleted from cache.")
        return ServiceResponse(status=False, message=f"Obtained datum belong to Logger with ID  {logger_id} not found in cache.")
