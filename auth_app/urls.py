from django.urls import path
from .controllers import *

app_name = 'auth_app'

urlpatterns = [
    path("login/", LoginController.as_view(), name='login'),
    path('register/', RegisterController.as_view(), name='register'),
    path('logout/', LogoutController.as_view(), name='logout'),
]
