from typing import TYPE_CHECKING
from django.http import JsonResponse, HttpResponseRedirect
from django.views.decorators.http import require_http_methods
from components.http_errors import custom_403
from project.namespace import TemplateNamespace
from .helpers import extract_user_data
from logger_app.controllers import LoggerController
from logger_app.cache import LoggerCache
from logger_app.models import LoggerModel
from django.shortcuts import render
from .controllers.obtained_data import ObtainedDataController

if TYPE_CHECKING:
    import uuid


@require_http_methods(["GET"])
def redirect_to_destination(request, dynamic_id):
    """
    Redirects to the destination URL if the logger entry exists.
    Logs metadata in ObtainedDataModel.
    """
    # not using LoggerController and working with LoggerModel directly.
    try:
        logger_entry = LoggerModel.objects.get(id=dynamic_id)
    except LoggerModel.DoesNotExist:
        return JsonResponse({"error": "Destination not found"}, status=404)

    # Log request metadata
    extract_user_data(request, logger_entry)
    # delete old cache of logger
    LoggerCache.delete_logger(logger_id=logger_entry.id)

    # Redirect to destination
    return HttpResponseRedirect(logger_entry.destination)



@require_http_methods(["GET"])
def display_obtained_data(request, logger_id: "uuid.UUID"):
    # checking if user has access to data. comparing user_id from session vs user_id of LoggerModel
    if request.session['user_id'] != str(LoggerController.find_logger(logger_id).data.user.id):
        return custom_403(request)

    # if user has access to data
    obtained_data = ObtainedDataController.find_obtained_data(logger_id)

    if obtained_data:
        return render(request, TemplateNamespace.gathered_data, {'data': obtained_data.data})
    else:
        return render(request, TemplateNamespace.gathered_data, {'message': obtained_data.message})
