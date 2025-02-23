from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpRequest
from typing import TYPE_CHECKING
from project.namespace import ReverseNamespace, TemplateNamespace
from sessions import verify_session
from logger_app.controllers import LoggerController
from obtained_data_app.controllers.obtained_data import ObtainedDataController

if TYPE_CHECKING:
    from logger_app.models import LoggerModel
    from service_response import ServiceResponse


class DashboardView(View):
    def get(self, request: HttpRequest):
        """ Displays the dashboard page to auth-ed users, otherwise redirects the non-authed ones to login. """

        if verify_session(request):
            result: "ServiceResponse" = LoggerController.find_user_loggers(user_id=request.session['user_id'])
            loggers: list | list['LoggerModel'] = result.data if result else []

            # we return logger and the number of obtained data of it in a dict
            response: dict['LoggerModel': int] = dict()

            for logger in loggers:
                obtained_data: "ServiceResponse" = ObtainedDataController.find_obtained_datum(logger_id=logger.id)
                response[logger] = len(obtained_data.data) if obtained_data else 0

            context = {"loggers": response}
            return render(request, TemplateNamespace.dashboard, context)

        return redirect(ReverseNamespace.login)

    def post(self, request: HttpRequest):
        """ Handles the creation of a new logger from the 'Create Logger' form. """
        if verify_session(request):
            user_id = request.session['user_id']

            result = LoggerController.create(
                user_id=user_id,
                destination=request.POST.get('destination')
            )
            if result:
                return redirect(ReverseNamespace.dashboard)
            else:
                loggers_result = LoggerController.find_user_loggers(user_id=request.session['user_id'])

                loggers = {} if not loggers_result else loggers_result.data
                context = {"error_message": result.error, "loggers": loggers}
                return render(request, TemplateNamespace.dashboard, context)

        return redirect(ReverseNamespace.login)
