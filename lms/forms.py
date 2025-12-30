from django import forms
from .models import Submission

class SubmissionForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ['code']
        widgets = {
            'code': forms.Textarea(attrs={'class': 'code-editor', 'rows': 15, 'placeholder': 'Напишите ваш Python код здесь...'}),
        }
