from django import forms
from .models import Subject

class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['name', 'teacher']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nom de la matière'
            }),
            'teacher': forms.Select(attrs={
                'class': 'form-control'
            })
        }
        labels = {
            'name': 'Nom de la matière',
            'teacher': 'Enseignant'
        }