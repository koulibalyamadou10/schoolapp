from django.db import models

from student.models import Student
from subject.models import Subject


# Create your models here.
# ✅ Note
class Grade(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='grades')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='grades')
    grade = models.FloatField()
    date = models.DateField()

    def __str__(self):
        return f"{self.student} - {self.subject}: {self.grade}"