from service_response import ServiceResponse
import re
from user_app.controllers import UserController
from user_app.models import UserModel


def check_password_strength(password: str) -> ServiceResponse:
    """Check the strength of a password."""
    unmet_criteria = []

    if len(password) < 8:
        unmet_criteria.append("Password must be at least 8 characters long.")
    if not re.search(r'\d', password):
        unmet_criteria.append("Password must contain at least one digit (0-9).")
    if not re.search(r'[A-Z]', password):
        unmet_criteria.append("Password must contain at least one uppercase letter (A-Z).")
    if not re.search(r'[a-z]', password):
        unmet_criteria.append("Password must contain at least one lowercase letter (a-z).")
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        unmet_criteria.append("Password must contain at least one special character (!@#$%^&*(),.?\":{}|<>).")

    if unmet_criteria:
        return ServiceResponse(status=False, error={"unmet_criteria": unmet_criteria})

    return ServiceResponse(status=True)


class RegisterController:

    @staticmethod
    def create(username: str, password1: str, password2: str) -> ServiceResponse:
        """Does checks and registers a new user to db."""
        if password1 != password2:
            return ServiceResponse(status=False, data='password1', error='Passwords do not match')

        elif pswd_check := check_password_strength(password1) is False:
            return ServiceResponse(status=False, data='password1', error=pswd_check.error)

        elif UserModel.objects.filter(username=username).exists():
            return ServiceResponse(status=False, data='username', error=f'Username {username} is already taken.')

        else:
            UserController.register_user(username, password1)
            return ServiceResponse(status=True)
