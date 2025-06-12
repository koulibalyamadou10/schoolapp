from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from datetime import datetime, date
from .models import Teacher, Schedule, Attendance
from .forms import TeacherProfileForm, ScheduleForm, AttendanceForm
from subject.models import Subject
from student.models import Student
from grade.models import Grade
from account.decorators import role_required

@login_required
def teacher_profile(request):
    teacher = get_object_or_404(Teacher, user=request.user)
    if request.method == 'POST':
        form = TeacherProfileForm(request.POST, instance=teacher)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profil mis à jour avec succès')
            return redirect('teacher_profile')
    else:
        form = TeacherProfileForm(instance=teacher)
    return render(request, 'teacher/profile.html', {'form': form})

@login_required
def teacher_subjects(request):
    teacher = get_object_or_404(Teacher, user=request.user)
    subjects = Subject.objects.filter(teacher=teacher)
    return render(request, 'teacher/subjects.html', {'subjects': subjects})

@login_required
def teacher_schedule(request):
    teacher = get_object_or_404(Teacher, user=request.user)
    if request.method == 'POST':
        form = ScheduleForm(request.POST)
        if form.is_valid():
            schedule = form.save(commit=False)
            schedule.teacher = teacher
            schedule.save()
            messages.success(request, 'Cours ajouté à l\'emploi du temps')
            return redirect('teacher_schedule')
    else:
        form = ScheduleForm()
    
    schedules = Schedule.objects.filter(teacher=teacher).order_by('day_of_week', 'start_time')
    return render(request, 'teacher/schedule.html', {
        'form': form,
        'schedules': schedules
    })

@login_required
def manage_grades(request):
    teacher = get_object_or_404(Teacher, user=request.user)
    subjects = Subject.objects.filter(teacher=teacher)
    
    if request.method == 'POST':
        student_id = request.POST.get('student')
        subject_id = request.POST.get('subject')
        grade_value = request.POST.get('grade')
        
        if all([student_id, subject_id, grade_value]):
            student = Student.objects.get(id=student_id)
            subject = Subject.objects.get(id=subject_id)
            
            Grade.objects.create(
                student=student,
                subject=subject,
                grade=float(grade_value),
                date=date.today()
            )
            messages.success(request, 'Note ajoutée avec succès')
            return redirect('manage_grades')
    
    grades = Grade.objects.filter(subject__in=subjects).order_by('-date')
    students = Student.objects.all()
    
    return render(request, 'teacher/grades.html', {
        'subjects': subjects,
        'students': students,
        'grades': grades
    })

@login_required
def manage_attendance(request):
    teacher = get_object_or_404(Teacher, user=request.user)
    today = date.today()
    
    if request.method == 'POST':
        form = AttendanceForm(request.POST)
        if form.is_valid():
            attendance = form.save()
            messages.success(request, 'Présence enregistrée')
            return redirect('manage_attendance')
    else:
        form = AttendanceForm()
    
    schedules = Schedule.objects.filter(
        teacher=teacher,
        day_of_week=today.isoweekday()
    )
    
    attendances = Attendance.objects.filter(
        schedule__in=schedules,
        date=today
    ).select_related('student', 'schedule')
    
    return render(request, 'teacher/attendance.html', {
        'form': form,
        'schedules': schedules,
        'attendances': attendances,
        'today': today
    })

@login_required
@role_required(['teacher'])
def teacher_dashboard(request):
    teacher = get_object_or_404(Teacher, user=request.user)
    
    # Statistiques pour le tableau de bord
    subjects = Subject.objects.filter(teacher=teacher)
    total_students = Student.objects.filter(grades__subject__in=subjects).distinct().count()
    total_grades = Grade.objects.filter(subject__in=subjects).count()
    
    # Cours d'aujourd'hui
    today = date.today()
    classes_today = Schedule.objects.filter(
        teacher=teacher,
        day_of_week=today.isoweekday()
    ).count()
    
    context = {
        'teacher': teacher,
        'total_students': total_students,
        'total_subjects': subjects.count(),
        'total_grades': total_grades,
        'classes_today': classes_today,
    }
    return render(request, 'account/teacher_dashboard.html', context)