# authentication/forms.py
from django import forms
from .models import User
from project.models import Campus

class EditProfileForm(forms.ModelForm):
    campus = forms.ModelChoiceField(
        queryset=Campus.objects.all(),
        required=False,
        label='Campus',
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'id': 'campus-input',
            'placeholder': 'Digite o campus...',
            'autocomplete': 'off'
        })
    )

    class Meta:
        model = User
        fields = ['full_name', 'username', 'linkedin', 'github', 'about_me', 'image', 'campus']