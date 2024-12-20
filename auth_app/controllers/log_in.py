from components import ServiceResponse
from user_app.models import UserModel


class LoginController:
    @staticmethod
    def create(username, password):
        try:
            user = UserModel.objects.get(username=username)
        except UserModel.DoesNotExist:
            return ServiceResponse(status=False, error="User not found.")

        if not user.check_password(password):
            return ServiceResponse(status=False, error="Invalid login or password.")

        return ServiceResponse(status=True, data=user)
