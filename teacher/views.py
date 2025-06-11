from django.shortcuts import render, redirect
from django.utils import timezone
from django.core.exceptions import PermissionDenied
from account.decorators import role_required
from subject.models import Subject
from student.models import Student
from grade.models import Grade

@role_required(['teacher'])
@role_required(['teacher'])
def teacher_dashboard(request):
    teacher = request.user.teacher
    subjects = Subject.objects.filter(teacher=teacher)

    if request.method == "POST":
        # Récupération des données du formulaire modal
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        specialty = request.POST.get('specialty')

        # Validation simple (tu peux améliorer si tu veux)
        if first_name and last_name and specialty:
            teacher.first_name = first_name
            teacher.last_name = last_name
            teacher.specialty = specialty
            teacher.save()
            # Optionnel : message succès avec django.contrib.messages
            # messages.success(request, "Profil mis à jour avec succès")
            return redirect('teacher_dashboard')

        # Sinon, tu peux gérer les erreurs ici

    return render(request, 'teacher/dashboard.html', {
        'teacher': teacher,
        'subjects': subjects,
    })


@role_required(['teacher'])
def students_by_class(request):
    teacher = request.user.teacher
    subjects = Subject.objects.filter(teacher=teacher)
    students = Student.objects.filter(grades__subject__in=subjects).distinct()

    grouped_classes = {}
    for student in students:
        grouped_classes.setdefault(student.student_class, []).append(student)

    return render(request, 'teacher/students_by_class.html', {
        'classes': grouped_classes
    })

@role_required(['teacher'])
def enter_grade(request):
    teacher = request.user.teacher
    subjects = Subject.objects.filter(teacher=teacher)
    students = Student.objects.all()

    if request.method == "POST":
        student_id = request.POST.get("student")
        subject_id = request.POST.get("subject")
        grade_value = request.POST.get("grade")

        if student_id and subject_id and grade_value:
            student = Student.objects.get(id=student_id)
            subject = Subject.objects.get(id=subject_id)
            Grade.objects.create(
                student=student,
                subject=subject,
                grade=grade_value,
                date=timezone.now()
            )
            return redirect('enter_grade')

    return render(request, 'teacher/enter_grade.html', {
        'subjects': subjects,
        'students': students
    })


