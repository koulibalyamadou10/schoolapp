from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.utils import timezone
from django.urls import reverse
from datetime import datetime, time, timedelta
from .forms import UserRegistrationForm, UserProfileForm
from .models import User
from .decorators import role_required

def unauthorized_view(request):
    return render(request, 'account/401.html', status=401)

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('account:profile')
        else:
            messages.error(request, 'Identifiants invalides')
    return render(request, 'account/login.html')

def register_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            messages.success(request, 'Compte créé avec succès')
            return redirect('account:login')
    else:
        form = UserRegistrationForm()
    return render(request, 'account/register.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    return redirect('account:login')

@login_required
def profile_view(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profil mis à jour avec succès')
            return redirect('account:profile')
    else:
        form = UserProfileForm(instance=request.user)
    return render(request, 'account/profile.html', {'form': form})

@login_required
def change_password_view(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Votre mot de passe a été changé avec succès')
            return redirect('account:profile')
        else:
            messages.error(request, 'Veuillez corriger les erreurs ci-dessous')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'account/change_password.html', {'form': form})

def password_reset_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            reset_url = request.build_absolute_uri(
                reverse('password_reset_confirm', kwargs={'uidb64': uid, 'token': token})
            )
            
            subject = 'Réinitialisation de votre mot de passe'
            message = render_to_string('account/password_reset_email.html', {
                'user': user,
                'reset_url': reset_url,
            }, request)
            
            send_mail(subject, message, 'noreply@schoolapp.com', [user.email])
            messages.success(request, 'Les instructions de réinitialisation ont été envoyées à votre adresse e-mail')
            return redirect('login')
        except User.DoesNotExist:
            messages.error(request, 'Aucun compte trouvé avec cette adresse e-mail')
    
    return render(request, 'account/password_reset.html')

def password_reset_confirm_view(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            password1 = request.POST.get('new_password1')
            password2 = request.POST.get('new_password2')
            
            if password1 and password2 and password1 == password2:
                user.set_password(password1)
                user.save()
                messages.success(request, 'Votre mot de passe a été réinitialisé avec succès')
                return redirect('login')
            else:
                messages.error(request, 'Les mots de passe ne correspondent pas')
        
        return render(request, 'account/password_reset_confirm.html', {'validlink': True})
    else:
        return render(request, 'account/password_reset_confirm.html', {'validlink': False})

@login_required
@role_required(['admin'])
def admin_dashboard(request):
    from django.db.models import Count, Avg, Q
    from student.models import Student, AcademicRecord
    from teacher.models import Teacher, Attendance
    from subject.models import Subject
    from grade.models import Grade
    
    # Statistiques de base
    context = {
        'total_students': Student.objects.count(),
        'total_teachers': Teacher.objects.count(),
        'total_subjects': Subject.objects.count(),
        'total_grades': Grade.objects.count(),
    }
    
    # Répartition des étudiants par classe
    students_by_class = Student.objects.values('student_class').annotate(
        count=Count('id')
    ).order_by('student_class')
    context['students_by_class'] = students_by_class
    
    # Moyenne générale par classe
    class_averages = AcademicRecord.objects.values('student__student_class').annotate(
        avg_grade=Avg('average_grade')
    ).order_by('-avg_grade')
    context['class_averages'] = class_averages
    
    # Taux de présence global
    total_attendance = Attendance.objects.count()
    present_attendance = Attendance.objects.filter(
        Q(status='present') | Q(status='late')
    ).count()
    context['attendance_rate'] = (present_attendance / total_attendance * 100) if total_attendance > 0 else 0
    
    # Top 5 des matières avec les meilleures moyennes
    subject_averages = Grade.objects.values('subject__name').annotate(
        avg_grade=Avg('grade')
    ).order_by('-avg_grade')[:5]
    context['top_subjects'] = subject_averages
    
    # Répartition des statuts académiques
    academic_status = Student.objects.values('academic_status').annotate(
        count=Count('id')
    ).order_by('academic_status')
    context['academic_status'] = academic_status
    
    # Activités récentes (dernières 7 jours)
    seven_days_ago = timezone.now().date() - timedelta(days=7)

    # Dernières notes
    recent_grades = Grade.objects.select_related('student', 'subject').filter(
        date__gte=seven_days_ago
    ).order_by('-date')[:3]
    
    # Dernières absences
    recent_attendance = Attendance.objects.select_related('student', 'schedule__subject').filter(
        date__gte=seven_days_ago,
        status='absent'
    ).order_by('-date')[:3]
    
    # Derniers étudiants inscrits
    recent_students = Student.objects.filter(
        registration_date__gte=seven_days_ago
    ).order_by('-registration_date')[:3]
    
    # Activités récentes combinées
    recent_activities = []
    
    # Fonction pour convertir une date en datetime
    def to_datetime(date_obj):
        if isinstance(date_obj, datetime):
            return date_obj
        return datetime.combine(date_obj, time(0, 0))
    
    # Ajouter les notes récentes
    for grade in recent_grades:
        recent_activities.append({
            'type': 'grade',
            'icon': 'fas fa-star',
            'icon_class': 'new-grade',
            'text': f"Nouvelle note en {grade.subject.name}",
            'description': f"{grade.student.get_full_name()} a obtenu {grade.grade}/20",
            'date': to_datetime(grade.date)
        })
    
    # Ajouter les absences récentes
    for attendance in recent_attendance:
        recent_activities.append({
            'type': 'attendance',
            'icon': 'fas fa-user-times',
            'icon_class': 'absence',
            'text': "Absence enregistrée",
            'description': f"{attendance.student.get_full_name()} - {attendance.schedule.subject.name}",
            'date': to_datetime(attendance.date)
        })
    
    # Ajouter les nouveaux étudiants
    for student in recent_students:
        recent_activities.append({
            'type': 'new_student',
            'icon': 'fas fa-user-plus',
            'icon_class': 'new-student',
            'text': "Nouvel étudiant inscrit",
            'description': f"{student.get_full_name()} en {student.student_class}",
            'date': to_datetime(student.registration_date)
        })
    
    # Trier toutes les activités par date et garder les 5 plus récentes
    recent_activities.sort(key=lambda x: x['date'], reverse=True)
    context['recent_activities'] = recent_activities[:5]
    
    return render(request, 'account/admin_dashbord.html', context)
