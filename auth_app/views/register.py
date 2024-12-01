from django.shortcuts import render, redirect, reverse
from django.views import View
from django.contrib.auth.forms import UserCreationForm
from project.paths import TemplatePaths, Reverses
from auth_app.controllers import RegisterController


class RegisterView(View):
    def get(self, request):
        """ Redirects to dashboard page auth-ed users, renders the page with form for non-authed ones. """
        if request.user.is_authenticated:
            return redirect(reverse(Reverses.dashboard))

        form = UserCreationForm()
        return render(request, TemplatePaths.register, {'form': form})

    def post(self, request):
        form = UserCreationForm(request.POST)

        if form.is_valid():
            result = RegisterController.create(
                username=form.cleaned_data['username'],
                password1=form.cleaned_data['password1'],
                password2=form.cleaned_data['password2']
            )

            if not result:
                form.add_error(field=result.data, error=result.error)
            else:
                return redirect(reverse(Reverses.login))
        else:
            return render(request, TemplatePaths.register, {'form': form})
