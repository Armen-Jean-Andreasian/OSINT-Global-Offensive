from django.shortcuts import render
from project.namespace import ReverseNamespace
from project.namespace import TemplateNamespace


def custom_404(request, exception=None):
    return render(request, TemplateNamespace.resp_404, {'login_url': ReverseNamespace.login}, status=404)
