from django.shortcuts import render, redirect
from django.views import View
from project.paths import TemplatePaths, Reverses
from django.http import HttpRequest
from sessions import verify_session
from dashboard_app.controllers import DashboardController


class DashboardView(View):
    def get(self, request: HttpRequest):
        """ Displays the dashboard page to auth-ed users, otherwise redirects the non-authed ones to login. """

        if verify_session(request):
            result = DashboardController.get_loggers(user_id=request.session['user_id'])
            loggers = {} if not result else result.data
            context = {"loggers": loggers}
            return render(request, TemplatePaths.dashboard, context)

        return redirect(Reverses.login)

    def post(self, request: HttpRequest):
        """ Handle the creation of a new logger from the 'Create Logger' form. """
        if verify_session(request):
            user_id = request.session['user_id']

            result = DashboardController.create_logger(
                user_id=user_id,
                destination=request.POST.get('destination')
            )
            if result:
                return redirect(Reverses.dashboard)
            else:
                loggers_result = DashboardController.get_loggers(user_id=request.session['user_id'])

                loggers = {} if not loggers_result else loggers_result.data
                context = {"error_message": result.error, "loggers": loggers}
                return render(request, TemplatePaths.dashboard, context)

        return redirect(Reverses.login)
