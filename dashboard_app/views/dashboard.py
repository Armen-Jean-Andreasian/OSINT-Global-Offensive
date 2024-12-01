from django.shortcuts import render, redirect
from django.views import View
from project.config import TemplatePaths, Reverses
from django.http import HttpRequest
from sessions import verify_session


class DashboardController(View):
    def get(self, request: HttpRequest):
        """ Displays the dashboard page to auth-ed users, otherwise redirects the non-authed ones to login. """

        if verify_session(request):
            # TODO: retrieve user loggers and pass to dashboard.html using jinja
            # like result =  SELECT * FROM Logger where user.id = user_id
            # then render(request, TemplatePaths.dashboard, loggers=result)
            return render(request, TemplatePaths.dashboard)

        return redirect(Reverses.login)
