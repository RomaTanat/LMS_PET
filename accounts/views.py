from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required

from accounts.forms import RegistrationForm, UserForm, ProfileForm


# Регистрация
def register_view(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("user_profile")
    else:
        form = RegistrationForm()
    return render(request, "accounts/register.html", {"form": form})


# Логин
def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("user_profile")  # После логина переходим в профиль
    else:
        form = AuthenticationForm()
    return render(request, "accounts/login.html", {"form": form})

# Выход
def logout_view(request):
    logout(request)
    return redirect("login")

# Профиль (доступен только авторизованным)
@login_required
def profile_view(request):
    return redirect('user_profile')

@login_required
def edit_profile(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        # Check if profile exists before accessing it
        if hasattr(request.user, 'profile'):
            profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        else:
             # Handle missing profile if necessary, or create one
             # For now, assuming it exists or let it fail if not created by signal
            from .models import Profile
            profile, created = Profile.objects.get_or_create(user=request.user)
            profile_form = ProfileForm(request.POST, request.FILES, instance=profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('user_profile')
    else:
        user_form = UserForm(instance=request.user)
        if hasattr(request.user, 'profile'):
            profile_form = ProfileForm(instance=request.user.profile)
        else:
            from .models import Profile
            profile, created = Profile.objects.get_or_create(user=request.user)
            profile_form = ProfileForm(instance=profile)

    return render(request, 'accounts/edit_profile.html', {'user_form': user_form, 'profile_form': profile_form})
