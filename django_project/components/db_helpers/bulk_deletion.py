from service_response import ServiceResponse
from typing import TYPE_CHECKING, Union

if TYPE_CHECKING:
    from django.db.models.query import QuerySet
    from django.db.models import Model


def bulk_deletion(model: "Model", **query) -> ServiceResponse:
    """
    Perform a bulk deletion operation on a Django model, and return a ServiceResponse object
    indicating the success or failure of the deletion. In case of a failure, it provides
    additional information about the remaining records and any errors encountered.

    Parameters:
        model (Model): The Django model class on which the deletion operation will be performed.
        **query (dict): The filtering criteria to select records for deletion. These are passed as keyword arguments to the `filter` method of the model.

    Returns:
        Union[ServiceResponse[bool, str, dict[str:list], ServiceResponse[bool, str, str, dict[str:list]]]:
            - On success: A `ServiceResponse` with `status=True`, a message indicating how many records were deleted, and an empty list.
            - On failure: A `ServiceResponse` with `status=False`, a failure message indicating how many records were deleted successfully
              before the failure, the error message, and the list of records that could not be deleted.

    Example:
        # Example usage:
        response: ServiceResponse = bulk_deletion(MyModel, field=value)
        if response:
            print(f"{response.message}")
        else:
            print(f"Error: {response.message}. Remaining records: {response.data}")
    """

    found_models_from_db: "QuerySet" = model.objects.filter(**query)

    if not found_models_from_db.exists():
        return ServiceResponse(status=False, message="Empty query", data=[])

    total_to_delete: int = found_models_from_db.count()

    try:  # bulk deletion
        removed_data_count, _ = found_models_from_db.delete()  # returns count and details of deleted records
    except Exception as err:
        obj_left_to_delete: "QuerySet" = model.objects.filter(**query)
        left_to_delete: int = total_to_delete - obj_left_to_delete.count()

        obj_left_to_delete_list = list(obj_left_to_delete)

        deleted_records = [record for record in list(found_models_from_db) if record not in obj_left_to_delete_list]

        return ServiceResponse(
            status=False,
            message=f"Failed to delete records. {left_to_delete} out of {total_to_delete} were deleted.",
            error=str(err),
            data={"deleted": deleted_records, "left_to_delete": obj_left_to_delete_list}
        )
    else:
        return ServiceResponse(
            status=True,
            message=f"{removed_data_count} data records deleted.",
            data={"deleted": list(found_models_from_db), "left_to_delete": []}
        )
