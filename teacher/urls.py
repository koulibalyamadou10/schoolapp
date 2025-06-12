
from django.urls import path
from . import views

app_name = 'teacher'

urlpatterns = [
    # Gestion du profil enseignant
    path('profile/', views.teacher_profile, name='profile'),
    
    # Gestion des matières
    path('subjects/', views.teacher_subjects, name='subjects'),
    
    # Gestion de l'emploi du temps
    path('schedule/', views.teacher_schedule, name='schedule'),
    
    # Gestion des notes
    path('grades/', views.manage_grades, name='grades'),
    
    # Gestion des présences
    path('attendance/', views.manage_attendance, name='attendance'),
]
