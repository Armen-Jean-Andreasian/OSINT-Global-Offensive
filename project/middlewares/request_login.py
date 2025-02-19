from django.shortcuts import redirect
from project.urls import PATH_FOR_FISH
from auth_app.apps import AuthAppConfig
from django.urls import resolve
import logging

logger = logging.getLogger(__name__)


class RequireLoginMiddleware:
    """
    For authentication, we do check the user permissions through the session's user_id.
    However, if the user_id is not present in the session, it will throw an error, we redirect the user to the login page.

    Also, we are excluding the auth_app from this middleware, as it will be the only way to log in.
    And we are excluding the PATH_FOR_FISH from this middleware, as it is designed to not require authentication to gather IP data.

    Redirects to / path if no user_id in session for all routes,
    except for paths from auth_app or starting with PATH_FOR_FISH.
    """

    def __init__(self, get_response):
        logger.info("🔥 RequireLoginMiddleware initialized!")
        self.get_response = get_response
        self.auth_app_name = AuthAppConfig.name  # Made this one instance var for quick access

    def __call__(self, request):
        requested_path = request.path

        logger.info(f"📢 REQUESTED PATH: {requested_path}")

        # Getting `resolver_match` identify to determine which application the path belongs to
        resolver_match = resolve(requested_path)

        # If one of auth app's urls was requested, or it was starting with obtain_data - proceed
        if resolver_match.app_name == self.auth_app_name or request.path.startswith(PATH_FOR_FISH):
            return self.get_response(request)

        # Checking if user_id is given for the entire project. If it's not redirecting to /
        if not request.session.get("user_id"):
            return redirect('auth_app:login')
        return self.get_response(request)
