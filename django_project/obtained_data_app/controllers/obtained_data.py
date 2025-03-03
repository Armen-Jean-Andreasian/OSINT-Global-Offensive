from service_response import ServiceResponse
from ..models import ObtainedDataModel
from typing import TYPE_CHECKING
from ..cache import ObtainedDataCache
from components.db_helpers import bulk_deletion

if TYPE_CHECKING:
    from uuid import UUID


class ObtainedDataController:
    cache = ObtainedDataCache

    @classmethod
    def find_obtained_datum(cls, logger_id: "UUID") -> ServiceResponse:
        """
        Finds all obtained data of a logger with given id.
        First it looks for obtained data in the cache by logger_id, if not found, then looks in the database.
        """
        datum_from_redis: ServiceResponse = cls.cache.get_obtained_datum(logger_id)

        # if not found in cache
        if not datum_from_redis:
            # look in the database
            found_datum_db: list = list(ObtainedDataModel.objects.filter(logger__id=logger_id))
            # if not found in the database
            if not found_datum_db:
                return ServiceResponse(status=False, error="No obtained data found.")
            else:
                # if found in the database, save it to cache
                cls.cache.set_obtained_datum(logger_id, obtained_data_instances=found_datum_db)
                print("Obtained data found in DB.")
                return ServiceResponse(status=True, data=found_datum_db)
        else:
            print("Obtained data found in cache.")
            return ServiceResponse(status=True, data=datum_from_redis.data)

    @classmethod
    def delete_obtained_datum(cls, logger_id: "UUID") -> ServiceResponse:
        """
        Deletes all obtained data records of a logger with given id.

        Returns: ServiceResponse[bool, str, list], ServiceResponse[bool, str, str, list]

        """
        del_resp: ServiceResponse = bulk_deletion(model=ObtainedDataModel, logger__id=logger_id)

        # deleting obtained datum from cache in advance
        cls.cache.delete_obtained_datum(logger_id)

        if not del_resp:
            if not del_resp.data.get('left_to_delete'):
                return ServiceResponse(status=False, message=f"Obtained data for logger {logger_id} not found")

        return del_resp
