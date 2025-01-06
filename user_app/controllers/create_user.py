from service_response import ServiceResponse
from user_app.models import UserModel


class UserController:
    @staticmethod
    def register_user(username: str, password: str) -> ServiceResponse:
        # this check is implemented in RegisterController, however, leaving this here, just in case.
        if UserModel.objects.filter(username=username).exists():
            return ServiceResponse(status=False, error=f'Username {username} is already taken.')

        user = UserModel(username=username)
        user.set_password(password)
        user.save()
        return ServiceResponse(status=True, data=user)
