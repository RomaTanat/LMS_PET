from django.contrib.auth import logout
from django.shortcuts import redirect
from django.urls import path
from .views import login_view, logout_view, register_view, profile_view, edit_profile


def custom_logout(request):
    logout(request)  # Разлогиниваем пользователя
    return redirect("home")
urlpatterns = [
    path("login/", login_view, name="login"),
    path("logout/", custom_logout, name="logout"),
    path("register/", register_view, name="register"),
    path("profile/", profile_view, name="profile"),
    path('profile/edit/', edit_profile, name='edit_profile'),
]
