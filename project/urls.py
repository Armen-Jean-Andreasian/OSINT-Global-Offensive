from django.contrib import admin
from django.urls import path, include, re_path
from django.shortcuts import redirect
from django.conf import settings
from django.conf.urls.static import static
import os


def redirect_to_login(request):
    return redirect('auth_app:login')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('auth_app.urls')),
    path('profile/', include('dashboard_app.urls')),
    re_path(r'^.*$', redirect_to_login),  # match all other (undefined) paths and redirecting to login page
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=os.path.join(settings.BASE_DIR, 'shared_static'))
