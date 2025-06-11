from django.db import models

from account.models import User


# Create your models here.
# ✅ Enseignant
class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='teacher')
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    specialty = models.CharField(max_length=100)

    def __str__(self):
        return f"Pr. {self.first_name} {self.last_name} - {self.specialty}"