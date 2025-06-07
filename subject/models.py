from django.db import models

from teacher.models import Teacher


# Create your models here.
# ✅ Matière
class Subject(models.Model):
    name = models.CharField(max_length=100)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='subjects')

    def __str__(self):
        return f"{self.name} (enseigné par {self.teacher})"