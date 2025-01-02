from django.shortcuts import render, redirect, reverse
from django.views import View
from django.contrib import messages
from project.namespace.reverse_namespace import ReverseNamespace
from project.namespace.template_namespace import TemplateNamespace
from sessions import verify_session
from auth_app.controllers import LoginController


class LoginView(View):
    def get(self, request):
        """Redirects to dashboard page for authenticated users, renders the page for non-authenticated ones."""
        if verify_session(request):
            return redirect(ReverseNamespace.dashboard)
        return render(request, TemplateNamespace.login)

    def post(self, request):
        username = request.POST.get('login')
        password = request.POST.get('password')
        result = LoginController.create(username, password)

        if not result:
            messages.error(request, result.error)
            return render(request, TemplateNamespace.login)

        # Regenerate session key to prevent fixation attacks
        request.session.cycle_key()
        request.session.save()

        user = result.data
        request.session['user_id'] = str(user.id)
        return redirect(reverse(ReverseNamespace.dashboard))
