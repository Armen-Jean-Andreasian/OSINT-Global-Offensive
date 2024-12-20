from django.shortcuts import render, redirect
from django.views import View
from project.paths import TemplatePaths, Reverses
from django.http import HttpRequest
from sessions import verify_session
from logger_app.controllers import LoggerController


class DashboardView(View):
    def get(self, request: HttpRequest):
        """ Displays the dashboard page to auth-ed users, otherwise redirects the non-authed ones to login. """

        if verify_session(request):
            result = LoggerController.find_user_loggers(user_id=request.session['user_id'])
            loggers: list = [] if not result else result.data
            print(type(loggers[1]))
            # logger : entry
            # if entries_found := len(loggers)

            context = {"loggers": loggers}
            return render(request, TemplatePaths.dashboard, context)

        return redirect(Reverses.login)

    def post(self, request: HttpRequest):
        """ Handle the creation of a new logger from the 'Create Logger' form. """
        if verify_session(request):
            user_id = request.session['user_id']

            result = LoggerController.create(
                user_id=user_id,
                destination=request.POST.get('destination')
            )
            if result:
                return redirect(Reverses.dashboard)
            else:
                loggers_result = LoggerController.find_user_loggers(user_id=request.session['user_id'])

                loggers = {} if not loggers_result else loggers_result.data
                context = {"error_message": result.error, "loggers": loggers}
                return render(request, TemplatePaths.dashboard, context)

        return redirect(Reverses.login)
