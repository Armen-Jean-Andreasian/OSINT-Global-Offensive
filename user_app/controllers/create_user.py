from user_app.models import UserModel
from project_components import ServiceResponse


class UserController:
    @staticmethod
    def register_user(username: str, password: str) -> ServiceResponse:
        if UserModel.objects.filter(username=username).exists():
            return ServiceResponse(status=False, error=f'Username {username} is already taken.')

        user = UserModel(username=username)
        user.set_password(password)
        user.save()
        return ServiceResponse(status=True, data=user)
