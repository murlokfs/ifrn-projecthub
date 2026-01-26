from django import forms
from .models import Project
from ckeditor_uploader.widgets import CKEditorUploadingWidget

class ProjectForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = Project
        fields = ['title', 'image', 'course', 'type', 'description', 'orientators', 'is_private', 'tags', 'members', 'link_github', 'link_youtube']

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Ex: Nome do Projeto'}),
            'image': forms.FileInput(attrs={'id': 'id_image'}),
            'type': forms.Select(attrs={'class': 'form-input'}),
            'link_github': forms.URLInput(attrs={'class': 'form-input has-icon', 'placeholder': 'Ex.: https://github.com/murlokfs/ifrn-projecthub'}),
            'link_youtube': forms.URLInput(attrs={'class': 'form-input has-icon', 'placeholder': 'Ex.: https://www.youtube.com/watch?v=xrEvNTEtrQ4'}),
            # Ocultando os selects para controle via JavaScript/Modal
            'members': forms.SelectMultiple(attrs={'id': 'id_members'}),
            'orientators': forms.SelectMultiple(attrs={'id': 'id_orientators'}),
            'tags': forms.SelectMultiple(attrs={'id': 'id_tags'}),
        }