from django.contrib import admin
from django.urls import path, include, re_path
from components.http_errors import custom_404

# this path should be excluded from auth.
PATH_FOR_FISH = 'obtain_data/'
LOGIN_PAGE = '/auth'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('auth_app.urls')),
    path('profile/', include('dashboard_app.urls')),
    path('obtain_data/', include('obtained_data_app.urls', namespace='obtained_data_app')),  # Add namespace here
    re_path(r'^(?!obtain_data).*$', lambda request: custom_404(request))  # redirect('auth_app:login') was removed
]
