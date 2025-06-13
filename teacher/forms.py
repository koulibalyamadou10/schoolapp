from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from django.conf import settings
from account.models import User
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

class TeacherCreationForm(forms.ModelForm):
    first_name = forms.CharField(
        max_length=100, 
        label="Prénom",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    last_name = forms.CharField(
        max_length=100, 
        label="Nom",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    specialty = forms.CharField(
        max_length=100, 
        label="Spécialité",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']
        labels = {
            'username': "Nom d'utilisateur",
            'email': 'Email',
        }
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def save(self, commit=True):
        user = self.instance
        user.username = self.cleaned_data['username']
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.role = 'teacher'
        
        # Générer un mot de passe temporaire
        user.set_password('admin123')
        
        if commit:
            user.save()
            
            # Créer le profil enseignant
            Teacher.objects.create(
                user=user,
                first_name=self.cleaned_data['first_name'],
                last_name=self.cleaned_data['last_name'],
                specialty=self.cleaned_data['specialty']
            )
            
            # Envoyer l'email avec les informations de connexion
            self.send_credentials_email(user, 'admin123')
        
        return user
    
    def send_credentials_email(self, user, password):
        """Envoie les identifiants de connexion par email"""
        try:
            subject = 'Bienvenue - Vos identifiants de connexion'
            message = f"""
Bonjour {user.first_name} {user.last_name},

Votre compte enseignant a été créé avec succès.

Vos identifiants de connexion :
- Nom d'utilisateur : {user.username}
- Mot de passe temporaire : {password}

Veuillez vous connecter et changer votre mot de passe lors de votre première connexion.

URL de connexion : {getattr(settings, 'SITE_URL', 'http://localhost:8000')}/account/login/

Cordialement,
L'équipe administrative
            """

            print(f"=== DEBUG EMAIL ===")
            print(f"Destinataire : {user.email}")
            print(f"Expéditeur : {getattr(settings, 'DEFAULT_FROM_EMAIL', 'noreply@schoolapp.com')}")
            print(f"Backend email : {getattr(settings, 'EMAIL_BACKEND', 'Non configuré')}")
            print(f"Host email : {getattr(settings, 'EMAIL_HOST', 'Non configuré')}")
            print(f"Port email : {getattr(settings, 'EMAIL_PORT', 'Non configuré')}")
            print(f"==================")
            
            # Envoi de l'email
            result = send_mail(
                subject,
                message,
                getattr(settings, 'DEFAULT_FROM_EMAIL', 'noreply@schoolapp.com'),
                [user.email],
                fail_silently=False,
            )
            
            print(f"Résultat de l'envoi d'email : {result}")
            
            if result == 1:
                print("Email envoyé avec succès !")
            else:
                print("Échec de l'envoi de l'email")
                
        except Exception as e:
            # Log l'erreur mais ne fait pas échouer la création
            print(f"ERREUR lors de l'envoi de l'email : {e}")
            print(f"Type d'erreur : {type(e).__name__}")
            import traceback
            print(f"Traceback complet : {traceback.format_exc()}")


# Garder l'ancien formulaire pour la compatibilité si nécessaire
class TeacherCreationFormWithPassword(UserCreationForm):
    first_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    specialty = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'teacher'
        if commit:
            user.save()
            Teacher.objects.create(
                user=user,
                first_name=self.cleaned_data['first_name'],
                last_name=self.cleaned_data['last_name'],
                specialty=self.cleaned_data['specialty']
            )
        return user

class ScheduleForm(forms.ModelForm):
    class Meta:
        model = Schedule
        fields = ['subject', 'day_of_week', 'start_time', 'end_time', 'classroom']
        widgets = {
            'subject': forms.Select(attrs={'class': 'form-control'}),
            'day_of_week': forms.Select(attrs={'class': 'form-control'}),
            'start_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'classroom': forms.Select(attrs={'class': 'form-control'}),
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