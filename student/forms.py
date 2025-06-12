from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator
from .models import Student, AcademicRecord

class StudentRegistrationForm(forms.ModelForm):
    class Meta:
        model = Student
        exclude = ['user', 'is_active', 'academic_status']
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
            'medical_info': forms.Textarea(attrs={'rows': 3}),
            'allergies': forms.Textarea(attrs={'rows': 2}),
            'address': forms.Textarea(attrs={'rows': 3}),
        }

class StudentUpdateForm(forms.ModelForm):
    class Meta:
        model = Student
        exclude = ['user', 'registration_date', 'student_id']
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
            'medical_info': forms.Textarea(attrs={'rows': 3}),
            'allergies': forms.Textarea(attrs={'rows': 2}),
            'address': forms.Textarea(attrs={'rows': 3}),
        }

class AcademicRecordForm(forms.ModelForm):
    class Meta:
        model = AcademicRecord
        exclude = ['student', 'created_at', 'updated_at']
        widgets = {
            'comments': forms.Textarea(attrs={'rows': 3}),
        }

    def clean_academic_year(self):
        year = self.cleaned_data['academic_year']
        if not year.match(r'^\d{4}-\d{4}$'):
            raise forms.ValidationError("Le format de l'année académique doit être YYYY-YYYY (ex: 2023-2024)")
        start_year = int(year.split('-')[0])
        end_year = int(year.split('-')[1])
        if end_year != start_year + 1:
            raise forms.ValidationError("L'année de fin doit être l'année suivante de l'année de début")
        return year