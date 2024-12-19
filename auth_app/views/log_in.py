from django.shortcuts import render, redirect, reverse
from django.views import View
from project.paths import TemplatePaths, Reverses
from sessions import verify_session
from auth_app.controllers import LoginController
from django.contrib import messages
from django.contrib.staticfiles.storage import staticfiles_storage


class LoginView(View):
    def get(self, request):
        """Redirects to dashboard page for authenticated users, renders the page for non-authenticated ones."""
        if verify_session(request):
            return redirect(Reverses.dashboard)
        return render(request, TemplatePaths.login_template)

    def post(self, request):
        username = request.POST.get('login')
        password = request.POST.get('password')
        result = LoginController.create(username, password)

        if not result:
            messages.error(request, result.error)
            return render(request, TemplatePaths.login_template)

        # Regenerate session key to prevent fixation attacks
        request.session.cycle_key()
        request.session.save()

        user = result.data
        request.session['user_id'] = user.id
        return redirect(reverse(Reverses.dashboard))
