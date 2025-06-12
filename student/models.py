from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from account.models import User
from datetime import date

# Create your models here.
# ✅ Étudiant
class Student(models.Model):
    GENDER_CHOICES = [
        ('M', 'Masculin'),
        ('F', 'Féminin'),
    ]

    # Informations de base
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100, verbose_name='Prénom')
    last_name = models.CharField(max_length=100, verbose_name='Nom')
    birth_date = models.DateField(verbose_name='Date de naissance')
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, verbose_name='Genre')
    
    # Informations académiques
    student_class = models.CharField(max_length=100, verbose_name='Classe')  # ex: "3ème A"
    registration_date = models.DateField(auto_now_add=True, verbose_name='Date d\'inscription')
    student_id = models.CharField(max_length=20, unique=True, verbose_name='Numéro d\'étudiant')
    
    # Informations de contact
    address = models.TextField(verbose_name='Adresse')
    phone = models.CharField(max_length=15, verbose_name='Téléphone')
    emergency_contact = models.CharField(max_length=100, verbose_name='Contact d\'urgence')
    emergency_phone = models.CharField(max_length=15, verbose_name='Téléphone d\'urgence')
    
    # Informations médicales
    medical_info = models.TextField(blank=True, verbose_name='Informations médicales')
    allergies = models.TextField(blank=True, verbose_name='Allergies')
    
    # Statut académique
    is_active = models.BooleanField(default=True, verbose_name='Actif')
    academic_status = models.CharField(
        max_length=20,
        choices=[
            ('REGULAR', 'Régulier'),
            ('PROBATION', 'Probation'),
            ('SUSPENDED', 'Suspendu'),
        ],
        default='REGULAR',
        verbose_name='Statut académique'
    )

    class Meta:
        verbose_name = 'Étudiant'
        verbose_name_plural = 'Étudiants'

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.student_class}"

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def get_age(self):
        today = date.today()
        return today.year - self.birth_date.year - ((today.month, today.day) < (self.birth_date.month, self.birth_date.day))


class AcademicRecord(models.Model):
    SEMESTER_CHOICES = [
        (1, '1er Semestre'),
        (2, '2ème Semestre'),
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='academic_records')
    academic_year = models.CharField(max_length=9, verbose_name='Année académique')  # Format: 2023-2024
    semester = models.IntegerField(choices=SEMESTER_CHOICES, verbose_name='Semestre')
    average_grade = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(20)],
        verbose_name='Moyenne générale'
    )
    class_rank = models.IntegerField(verbose_name='Rang')
    attendance_rate = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        verbose_name="Taux de présence"
    )
    comments = models.TextField(blank=True, verbose_name='Commentaires')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Dossier académique'
        verbose_name_plural = 'Dossiers académiques'
        unique_together = ['student', 'academic_year', 'semester']
        ordering = ['-academic_year', '-semester']

    def __str__(self):
        return f"{self.student.get_full_name()} - {self.academic_year} - Semestre {self.semester}"