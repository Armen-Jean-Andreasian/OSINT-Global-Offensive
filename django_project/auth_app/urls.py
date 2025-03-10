from django.urls import path
from .views import *

app_name = 'auth_app'

urlpatterns = [
    path("login/", LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('logout/', LogoutController.as_view(), name='logout'),
]
