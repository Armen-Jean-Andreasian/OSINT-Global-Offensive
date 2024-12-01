from django.shortcuts import render, redirect, reverse
from django.views import View
from user_app.models import UserModel
from project.config import TemplatePaths, Reverses
from sessions import verify_session


class LoginController(View):
    def get(self, request):
        """Redirects to dashboard page for authenticated users, renders the page for non-authenticated ones."""

        if verify_session(request):
            return redirect(Reverses.dashboard)

        return render(request, TemplatePaths.login_template)

    def post(self, request):
        login_username = request.POST.get('login')
        password = request.POST.get('password')

        try:
            user = UserModel.objects.get(username=login_username)
        except UserModel.DoesNotExist:
            return render(request, TemplatePaths.login_template, {"error_message": "User not found."})

        if not user.check_password(password):
            return render(request, TemplatePaths.login_template, {"error_message": "Invalid login or password"})

        # Regenerate session key to prevent fixation attacks
        request.session.cycle_key()
        request.session.save()

        request.session['user_id'] = user.id
        return redirect(reverse(Reverses.dashboard))
