from django import forms
from django.contrib.auth import get_user_model
from .models import Submission

User = get_user_model()

class SubmissionForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ['code']
        widgets = {
            'code': forms.Textarea(attrs={'class': 'code-editor', 'rows': 15, 'placeholder': 'Напишите ваш Python код здесь...'}),
        }

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'bio', 'avatar']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-input w-full bg-black/20 border border-gray-600 rounded px-3 py-2 text-white outline-none focus:border-blue-500'}),
            'last_name': forms.TextInput(attrs={'class': 'form-input w-full bg-black/20 border border-gray-600 rounded px-3 py-2 text-white outline-none focus:border-blue-500'}),
            'email': forms.EmailInput(attrs={'class': 'form-input w-full bg-black/20 border border-gray-600 rounded px-3 py-2 text-white outline-none focus:border-blue-500'}),
            'bio': forms.Textarea(attrs={'class': 'form-input w-full bg-black/20 border border-gray-600 rounded px-3 py-2 text-white outline-none focus:border-blue-500', 'rows': 4}),
            'avatar': forms.FileInput(attrs={'class': 'form-input w-full text-white bg-black/20 border border-gray-600 rounded cursor-pointer'}),
        }
