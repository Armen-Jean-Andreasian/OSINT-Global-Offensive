from django.shortcuts import render, redirect
from django.views import View
from project.config import TemplatePaths, Reverses
from django.http import HttpRequest
from sessions import verify_authorized_session, set_session_key


class DashboardController(View):
    def get(self, request: HttpRequest):
        """ Displays the dashboard page to auth-ed users, otherwise redirects the non-authed ones to login. """
        set_session_key(request)

        if 'user_id' in request.session:
            if verify_authorized_session(request):
                return render(request, TemplatePaths.dashboard)

        return redirect(Reverses.login)
