from django.db.models.signals import post_save
from django.dispatch import receiver
from account.models import User  # adapte le chemin selon ton projet
from teacher.models import Teacher

@receiver(post_save, sender=User)
def create_teacher_profile(sender, instance, created, **kwargs):
    if created and instance.role == 'teacher':
        # Crée un profil Teacher uniquement si l'utilisateur est enseignant
        Teacher.objects.create(user=instance, specialty="À définir")
