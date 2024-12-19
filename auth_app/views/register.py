from django.shortcuts import render, redirect, reverse
from django.views import View
from django.contrib.auth.forms import UserCreationForm
from project.paths import TemplatePaths, Reverses
from auth_app.controllers import RegisterController
from django.contrib import messages


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

            if not result:  # if we caught errors on model level
                form.add_error(field=result.data, error=result.error)
                messages.error(request, "Registration failed. Please fix the errors below.")
            else:
                messages.success(request, "Registration successful! Please log in.")
                return render(request, TemplatePaths.register, {'form': form})
        else:
            # processing and displaying errors from form.is_valid
            for field, field_errors in form.errors.get_json_data().items():
                messages.error(request, '\n'.join([error_dict['message'] for error_dict in field_errors]))

            return render(request, TemplatePaths.register, {'form': form})
