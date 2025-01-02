import os

from components import ServiceResponse
from typing import TYPE_CHECKING
from django.conf import settings
from ..models import ObtainedDataModel

REDIS_CACHE = settings.CACHE


if TYPE_CHECKING:
    import uuid


class ObtainedDataController:
    @staticmethod
    def find_obtained_data(logger_id: "uuid.UUID") -> ServiceResponse:
        """
        Finds all obtained data of a logger with given id.
        First it looks for obtained data in the cache by logger_id, if not found, then looks in the database.
        """
        # if not found in cache
        if not (found_data_cache := REDIS_CACHE.get_instance(logger_id)):
            # look in the database
            found_data_db: list = list(ObtainedDataModel.objects.filter(logger__id=logger_id))
            # if not found in the database
            if not found_data_db:
                return ServiceResponse(status=False, error="No obtained data found.")
            else:
                # if found in the database, save it to cache
                REDIS_CACHE.add_instance(
                    instance_id=logger_id, instance=found_data_db, ttl=os.environ.get("REDIS_TTL_OBTAINED_DATA")
                )
                print("Found data:", found_data_db)
                print("Obtained data found in DB.")
                # Return found_data_db, not found_data_cache
                return ServiceResponse(status=True, data=found_data_db)
        else:
            print("Obtained data found in cache.")
            return ServiceResponse(status=True, data=found_data_cache)


    @staticmethod
    def delete_records(logger_id: "uuid.UUID") -> ServiceResponse:
        """
        Deletes all obtained data records of a logger with given id.
        """
        found_data_db = ObtainedDataModel.objects.filter(logger__id=logger_id)

        if not found_data_db:
            return found_data_db
        else:
            removed_data_count: int = 0
            try:
                for data in found_data_db:
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
