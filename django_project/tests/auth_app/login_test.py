import pytest
from django.urls import reverse
from user_app.models import UserModel


@pytest.mark.django_db
def test_login_success(client):
    user = UserModel.objects.create(username="testuser")
    user.set_password("securepassword", overwrite=True)
    user.save()

    response = client.post(reverse("auth_app:login"), {"login": "testuser", "password": "securepassword"})

    assert response.status_code == 302  # Ensure a redirect occurs
    assert response.url == reverse("dashboard")  # The user should be redirected to the dashboard
    assert client.session["user_id"] == str(user.id)  # Verify that the session contains the user ID


@pytest.mark.django_db
def test_login_invalid_password(client):
    user = UserModel.objects.create(username="testuser")
    user.set_password("securepassword", overwrite=True)
    user.save()

    response = client.post(reverse("auth_app:login"), {"login": "testuser", "password": "wrongpassword"})

    assert response.status_code == 200  # The page should reload without redirecting
    assert "Invalid login or password." in response.content.decode()  # The error message should be displayed


@pytest.mark.django_db
def test_login_user_not_found(client):
    response = client.post(reverse("auth_app:login"), {"login": "nonexistent", "password": "password"})

    assert response.status_code == 200  # The page should reload without redirecting
    assert "User not found." in response.content.decode()  # The error message should be displayed
