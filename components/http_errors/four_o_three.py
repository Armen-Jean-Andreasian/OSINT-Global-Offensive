from django.shortcuts import render
from project.namespace import ReverseNamespace
from project.namespace import TemplateNamespace


def custom_403(request):
    return render(request, TemplateNamespace.resp_403, {'login_url': ReverseNamespace.login}, status=403)
