from django.shortcuts import render, redirect, reverse
from django.views import View
from django.contrib.auth.forms import UserCreationForm
from django.http import JsonResponse
from user_app.controllers import UserController
from project.config import TemplatePaths, Reverses
from auth_app.helpers import check_password_strength


class RegisterController(View):
    def get(self, request):
        """ Redirects to dashboard page auth-ed users, renders the page with form for non-authed ones. """
        if request.user.is_authenticated:
            return redirect(reverse(Reverses.dashboard))

        form = UserCreationForm()
        return render(request, TemplatePaths.register, {'form': form})

    def post(self, request):
        form = UserCreationForm(request.POST)

        if form.is_valid():
            try:
                username, password1, password2 = (
                    form.cleaned_data['username'], form.cleaned_data['password1'], form.cleaned_data['password2']
                )

                if password1 != password2:
                    form.add_error('password1', 'Passwords do not match')

                elif not (password_check_result := check_password_strength(password1)):
                    form.add_error('password1', password_check_result.error)

                elif not (registration_result := UserController.register_user(username, password1)):
                    form.add_error('username', registration_result.error)

                else:
                    return redirect(reverse(Reverses.login))

            except Exception as e:
                return JsonResponse({"error": f"Error: {str(e)}"}, status=400)

        return render(request, TemplatePaths.register, {'form': form})
