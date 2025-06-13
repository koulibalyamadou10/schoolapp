from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.forms import UserCreationForm
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from django.conf import settings
from account.models import User
from .models import Student, AcademicRecord

class StudentCreationForm(forms.ModelForm):
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
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    student_class = forms.CharField(
        max_length=50,
        label="Classe",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    birth_date = forms.DateField(
        label="Date de naissance",
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    address = forms.CharField(
        label="Adresse",
        widget=forms.Textarea(attrs={'rows': 3, 'class': 'form-control'})
    )
    phone = forms.CharField(
        max_length=20,
        label="Téléphone",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    parent_name = forms.CharField(
        max_length=100,
        label="Nom du parent/tuteur",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    parent_phone = forms.CharField(
        max_length=20,
        label="Téléphone du parent/tuteur",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    medical_info = forms.CharField(
        required=False,
        label="Informations médicales",
        widget=forms.Textarea(attrs={'rows': 3, 'class': 'form-control'})
    )
    allergies = forms.CharField(
        required=False,
        label="Allergies",
        widget=forms.Textarea(attrs={'rows': 2, 'class': 'form-control'})
    )

    class Meta:
        model = Student
        fields = [
            'first_name', 'last_name', 'email', 'student_class', 'birth_date',
            'address', 'phone', 'parent_name', 'parent_phone', 'medical_info', 'allergies'
        ]

    def save(self, commit=True):
        # Créer un nouvel utilisateur
        username = f"{self.cleaned_data['first_name'].lower()}.{self.cleaned_data['last_name'].lower()}"
        base_username = username
        counter = 1
        
        # S'assurer que le nom d'utilisateur est unique
        while User.objects.filter(username=username).exists():
            username = f"{base_username}{counter}"
            counter += 1
            
        # Générer un mot de passe temporaire
        temporary_password = 'admin123'
        
        # Créer l'utilisateur
        user = User.objects.create_user(
            username=username,
            email=self.cleaned_data['email'],
            password=temporary_password,
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name'],
            role='student'
        )
        
        # Créer l'étudiant
        student = Student(
            user=user,
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name'],
            student_class=self.cleaned_data['student_class'],
            birth_date=self.cleaned_data['birth_date'],
            address=self.cleaned_data['address'],
            phone=self.cleaned_data['phone'],
            parent_name=self.cleaned_data['parent_name'],
            parent_phone=self.cleaned_data['parent_phone'],
            medical_info=self.cleaned_data['medical_info'],
            allergies=self.cleaned_data['allergies'],
            student_id=f"STD{Student.objects.count() + 1:04d}"
        )
        
        if commit:
            student.save()
            self.send_credentials_email(user, temporary_password)
            
        return student
    
    def send_credentials_email(self, user, password):
        """Envoie les identifiants de connexion par email"""
        try:
            subject = 'Bienvenue - Vos identifiants de connexion'
            message = f"""
Bonjour {user.first_name} {user.last_name},

Votre compte étudiant a été créé avec succès.

Vos identifiants de connexion :
- Nom d'utilisateur : {user.username}
- Mot de passe temporaire : {password}

Veuillez vous connecter et changer votre mot de passe lors de votre première connexion.

URL de connexion : {getattr(settings, 'SITE_URL', 'http://localhost:8000')}/account/login/

Cordialement,
L'équipe administrative
            """

            print(f"=== DEBUG EMAIL ÉTUDIANT ===")
            print(f"Destinataire : {user.email}")
            print(f"Expéditeur : {getattr(settings, 'DEFAULT_FROM_EMAIL', 'noreply@schoolapp.com')}")
            print(f"Backend email : {getattr(settings, 'EMAIL_BACKEND', 'Non configuré')}")
            print(f"Host email : {getattr(settings, 'EMAIL_HOST', 'Non configuré')}")
            print(f"Port email : {getattr(settings, 'EMAIL_PORT', 'Non configuré')}")
            print(f"============================")
            
            # Envoi de l'email
            result = send_mail(
                subject,
                message,
                getattr(settings, 'DEFAULT_FROM_EMAIL', 'noreply@schoolapp.com'),
                [user.email],
                fail_silently=False,
            )
            
            print(f"Résultat de l'envoi d'email étudiant : {result}")
            
            if result == 1:
                print("Email étudiant envoyé avec succès !")
            else:
                print("Échec de l'envoi de l'email étudiant")
                
        except Exception as e:
            # Log l'erreur mais ne fait pas échouer la création
            print(f"ERREUR lors de l'envoi de l'email étudiant : {e}")
            print(f"Type d'erreur : {type(e).__name__}")
            import traceback
            print(f"Traceback complet : {traceback.format_exc()}")

class StudentRegistrationForm(forms.ModelForm):
    class Meta:
        model = Student
        exclude = ['user', 'is_active', 'academic_status', 'student_id', 'registration_date']
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'medical_info': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'allergies': forms.Textarea(attrs={'rows': 2, 'class': 'form-control'}),
            'address': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Ajouter des classes Bootstrap à tous les champs
        for field in self.fields:
            if field not in self.Meta.widgets:
                if self.fields[field].widget.__class__.__name__ in ['TextInput', 'NumberInput', 'EmailInput', 'PasswordInput', 'Select']:
                    self.fields[field].widget.attrs.update({'class': 'form-control'})

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
