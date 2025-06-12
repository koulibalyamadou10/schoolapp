from django import forms
from .models import Teacher, Schedule, Attendance

class TeacherProfileForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ['first_name', 'last_name', 'specialty']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'specialty': forms.TextInput(attrs={'class': 'form-control'}),
        }

class ScheduleForm(forms.ModelForm):
    class Meta:
        model = Schedule
        fields = ['subject', 'day_of_week', 'start_time', 'end_time', 'classroom']
        widgets = {
            'subject': forms.Select(attrs={'class': 'form-control'}),
            'day_of_week': forms.Select(attrs={'class': 'form-control'}),
            'start_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'classroom': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')

        if start_time and end_time and start_time >= end_time:
            raise forms.ValidationError("L'heure de début doit être antérieure à l'heure de fin.")

        return cleaned_data

class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ['student', 'schedule', 'date', 'status', 'minutes_late', 'note']
        widgets = {
            'student': forms.Select(attrs={'class': 'form-control'}),
            'schedule': forms.Select(attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'minutes_late': forms.NumberInput(attrs={'class': 'form-control', 'min': '1', 'max': '120'}),
            'note': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def clean(self):
        cleaned_data = super().clean()
        status = cleaned_data.get('status')
        minutes_late = cleaned_data.get('minutes_late')

        if status == 'late' and not minutes_late:
            raise forms.ValidationError("Veuillez spécifier le nombre de minutes de retard.")
        elif status != 'late' and minutes_late:
            cleaned_data['minutes_late'] = None

        return cleaned_data