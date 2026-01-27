# authentication/forms.py
from django import forms
from .models import User

class EditProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['full_name', 'username', 'linkedin', 'github', 'about_me', 'image']
        # Nota: 'linkedin' substitui 'cidade' baseado no seu pedido