import re
from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.forms import UserCreationForm
from django.core.mail import send_mail, EmailMessage
from django.template.loader import render_to_string
from django.utils.crypto import get_random_string
from django.conf import settings
from account.models import User
from account.utils import generate_random_password
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
    student_class = forms.Select(attrs={'class': 'form-control'})
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
    emergency_contact = forms.CharField(
        max_length=100,
        label="Nom du parent/tuteur",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    emergency_phone = forms.CharField(
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
            'address', 'phone', 'emergency_contact', 'emergency_phone', 'medical_info', 'allergies'
        ]
        widgets = {
            'student_class': forms.Select(attrs={'class': 'form-control'}),
        }

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
        temporary_password = generate_random_password()
        
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
            emergency_contact=self.cleaned_data['emergency_contact'],
            emergency_phone=self.cleaned_data['emergency_phone'],
            medical_info=self.cleaned_data['medical_info'],
            allergies=self.cleaned_data['allergies'],
            student_id=f"STD{Student.objects.count() + 1:04d}"
        )
        
        if commit:
            student.save()
            send_credentials_email(user, temporary_password)
            
        return student
    

def send_credentials_email(user, password):
    """Envoie les identifiants de connexion par email"""
    try:
        email_subject = 'Bienvenue - Vos identifiants de connexion'
        
        context = {
            'user': user,
            'password': password,
            'login_url': f"{getattr(settings, 'SITE_URL', 'http://localhost:8001')}/",
            'company_name': getattr(settings, 'COMPANY_NAME', 'SchoolApp'),
        }
        
        # Chargement du template HTML
        email_body = render_to_string("emails/credentials_email.html", context)
        
        # Créer l'email
        email = EmailMessage(
            email_subject,
            email_body,
            settings.EMAIL_HOST_USER,
            [user.email],
        )

        email.content_subtype = 'html'  # Email en format HTML
        
        result = email.send(fail_silently=False)
        
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
        if not re.match(r'^\d{4}-\d{4}$', year):
            raise forms.ValidationError("Le format de l'année académique doit être YYYY-YYYY (ex: 2023-2024)")
        start_year, end_year = map(int, year.split('-'))
        if end_year != start_year + 1:
            raise forms.ValidationError("L'année de fin doit être l'année suivante de l'année de début")
        return year
