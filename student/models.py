from django.db import models

from account.models import User


# Create your models here.
# ✅ Étudiant
class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    birth_date = models.DateField()
    student_class = models.CharField(max_length=100)  # ex: "3ème A"

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.student_class}"