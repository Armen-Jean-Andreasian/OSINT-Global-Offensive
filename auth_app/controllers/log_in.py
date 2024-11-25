from django.shortcuts import render, redirect, reverse
from django.views import View
from user_app.models import UserModel
from project.config import TemplatePaths, Reverses
from sessions import verify_authorized_session, set_session_key


class LoginController(View):
    def get(self, request):
        """Redirects to dashboard page for authenticated users, renders the page for non-authenticated ones."""
        set_session_key(request)

        if 'user_id' in request.session:
            if verify_authorized_session(request):
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

        request.session['user_id'] = user.id

        return redirect(reverse(Reverses.dashboard))
