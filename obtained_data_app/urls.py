from django.urls import path
from . import views

urlpatterns = [
    path('<uuid:dynamic_id>/', views.redirect_to_destination, name='redirect_to_destination'),
]