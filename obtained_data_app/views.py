from logger_app.models import LoggerModel
from django.http import JsonResponse, HttpResponseRedirect
from django.views.decorators.http import require_http_methods
from django.shortcuts import render
from .helpers import extract_user_data
from .controllers.obtained_data import ObtainedDataController
from project.namespace import TemplateNamespace
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import uuid



@require_http_methods(["GET"])
def redirect_to_destination(request, dynamic_id):
    """
    Redirects to the destination URL if the logger entry exists.
    Logs metadata in ObtainedDataModel.
    """
    try:
        logger_entry = LoggerModel.objects.get(id=dynamic_id)
    except LoggerModel.DoesNotExist:
        return JsonResponse({"error": "Destination not found"}, status=404)

    # Log request metadata
    extract_user_data(request, logger_entry)

    # Redirect to destination
    return HttpResponseRedirect(logger_entry.destination)


@require_http_methods(["GET"])
def display_obtained_data(request, logger_id: "uuid.UUID"):
    obtained_data = ObtainedDataController.find_obtained_data(logger_id)

    if obtained_data:
        return render(request, TemplateNamespace.gathered_data, {'data': obtained_data.data})
    else:
        return render(request, TemplateNamespace.gathered_data, {'message': obtained_data.message})
