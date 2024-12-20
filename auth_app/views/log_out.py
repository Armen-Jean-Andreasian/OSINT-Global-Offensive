from django.shortcuts import redirect, reverse
from django.views import View
from project.namespace.reverse_namespace import ReverseNamespace


class LogoutController(View):
    def post(self, request):
        """Logs out the user by clearing their session and redirecting to the login page."""
        request.session.flush()
        return redirect(reverse(ReverseNamespace.login))
