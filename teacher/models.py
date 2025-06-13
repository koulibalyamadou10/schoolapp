from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from account.models import User


# Create your models here.
# ✅ Enseignant
class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    specialty = models.CharField(max_length=100)

    def __str__(self):
        return f"Pr. {self.first_name} {self.last_name} - {self.specialty}"


# ✅ Emploi du temps
class Schedule(models.Model):
    DAYS_OF_WEEK = [
        (1, 'Lundi'),
        (2, 'Mardi'),
        (3, 'Mercredi'),
        (4, 'Jeudi'),
        (5, 'Vendredi'),
        (6, 'Samedi'),
    ]

    STUDENT_CLASS_CHOICES = [
        ('6A', '6ème A'),
        ('6B', '6ème B'),
        ('5A', '5ème A'), 
        ('5B', '5ème B'),
        ('4A', '4ème A'),
        ('4B', '4ème B'),
        ('3A', '3ème A'),
        ('3B', '3ème B'),
        ('2A', '2nde A'),
        ('2B', '2nde B'),
        ('1A', '1ère A'),
        ('1B', '1ère B'),
        ('TA', 'Terminale A'),
        ('TB', 'Terminale B'),
    ]

    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='schedules')
    subject = models.ForeignKey('subject.Subject', on_delete=models.CASCADE)
    day_of_week = models.IntegerField(choices=DAYS_OF_WEEK)
    start_time = models.TimeField()
    end_time = models.TimeField()
    classroom = models.CharField(max_length=50, default='6A', choices=STUDENT_CLASS_CHOICES)

    class Meta:
        ordering = ['day_of_week', 'start_time']

    def __str__(self):
        return f"{self.get_day_of_week_display()} {self.start_time}-{self.end_time}: {self.subject} ({self.classroom})"


# ✅ Assiduité
class Attendance(models.Model):
    ATTENDANCE_STATUS = [
        ('present', 'Présent'),
        ('absent', 'Absent'),
        ('late', 'En retard'),
        ('excused', 'Absence justifiée'),
    ]

    student = models.ForeignKey('student.Student', on_delete=models.CASCADE)
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(max_length=10, choices=ATTENDANCE_STATUS)
    minutes_late = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(1), MaxValueValidator(120)])
    note = models.TextField(blank=True)

    class Meta:
        unique_together = ['student', 'schedule', 'date']
        ordering = ['-date', 'schedule']

    def __str__(self):
        return f"{self.student} - {self.schedule.subject} - {self.date}: {self.get_status_display()}"