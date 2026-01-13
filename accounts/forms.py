from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from accounts.models import Profile

# Получаем кастомную модель пользователя
User = get_user_model()

# Форма регистрации
class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email"]

# Дополнительная форма для добавления bio и avatar
class CustomUserCreationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'bio', 'avatar']

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar', 'priorities']
        widgets = {
            'priorities': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Например: Изучить Python, Освоить веб-разработку, Подготовиться к сертификации...'
            })
        }