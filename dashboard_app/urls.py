from django.urls import path
from .views import DashboardController

app_name = 'dashboard_app'


urlpatterns = [
    path('dashboard/', DashboardController.as_view(), name='dashboard'),
]
