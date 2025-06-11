from django.contrib.auth import get_user_model
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import CustomUserCreationForm  # À créer si besoin

User = get_user_model()

# -------------------------------
# CRUD UTILISATEURS
# -------------------------------

def user_list(request):
    users = User.objects.all()
    return render(request, 'account/user_list.html', {'users': users})

def user_create(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Utilisateur créé avec succès.")
            return redirect('user_list')
    else:
        form = CustomUserCreationForm()
    return render(request, 'account/user_form.html', {'form': form})

def user_update(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Utilisateur modifié avec succès.")
            return redirect('user_list')
    else:
        form = CustomUserCreationForm(instance=user)
    return render(request, 'account/user_form.html', {'form': form})

def user_delete(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        user.delete()
        messages.success(request, "Utilisateur supprimé avec succès.")
        return redirect('user_list')
    return render(request, 'account/user_confirm_delete.html', {'user': user})

# -------------------------------
# TABLEAU DE BORD ADMINISTRATEUR
# -------------------------------

from student.models import Student
from teacher.models import Teacher
from subject.models import Subject

def is_admin(user):
    return user.is_superuser or getattr(user, 'role', None) == 'admin'

@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    total_users = User.objects.count()
    total_students = Student.objects.count()
    total_teachers = Teacher.objects.count()
    total_subjects = Subject.objects.count()
    return render(request, 'account/admin_dashboard.html', {
        'total_users': total_users,
        'total_students': total_students,
        'total_teachers': total_teachers,
        'total_subjects': total_subjects,
    })
   
# -------------------------------
# TABLEAU DE BORD ADMINISTRATEUR - STATISTIQUES DES NOTES
# -------------------------------

from django.db.models import Avg
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render
from grade.models import Grade
from student.models import Student
from subject.models import Subject

def is_admin(user):
    return user.is_superuser or getattr(user, 'role', None) == 'admin'

@login_required
@user_passes_test(is_admin)
def admin_grades_stats(request):
    # Statistiques globales
    total_notes = Grade.objects.count()
    moyenne_generale = Grade.objects.aggregate(Avg('grade'))['grade__avg'] or 0

    # Statistiques par matière
    stats_par_matiere = []
    for subject in Subject.objects.all():
        notes = Grade.objects.filter(subject=subject)
        moyenne = notes.aggregate(Avg('grade'))['grade__avg'] or 0
        stats_par_matiere.append({
            'subject': subject,
            'count': notes.count(),
            'average': round(moyenne, 2),
        })

    # Liste des notes (avec jointure)
    notes = Grade.objects.select_related('student', 'subject').all().order_by('-id')[:50]

    return render(request, 'account/admin_grades_stats.html', {
        'total_notes': total_notes,
        'moyenne_generale': round(moyenne_generale, 2),
        'stats_par_matiere': stats_par_matiere,
        'notes': notes,
    })