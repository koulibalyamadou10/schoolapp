from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Student, AcademicRecord
from .forms import StudentRegistrationForm, StudentUpdateForm, AcademicRecordForm
from account.decorators import student_required, admin_required

@admin_required
def student_list(request):
    query = request.GET.get('q')
    students = Student.objects.all()
    
    if query:
        students = students.filter(
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(student_id__icontains=query) |
            Q(student_class__icontains=query)
        )
    
    paginator = Paginator(students, 10)
    page = request.GET.get('page')
    students = paginator.get_page(page)
    
    return render(request, 'student/student_list.html', {'students': students, 'query': query})

@admin_required
def student_create(request):
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            student = form.save(commit=False)
            # Générer un numéro d'étudiant unique
            student.student_id = f"STD{Student.objects.count() + 1:04d}"
            student.save()
            messages.success(request, 'Étudiant créé avec succès.')
            return redirect('student:student_detail', pk=student.pk)
    else:
        form = StudentRegistrationForm()
    
    return render(request, 'student/student_form.html', {'form': form, 'title': 'Créer un étudiant'})

@admin_required
def student_update(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        form = StudentUpdateForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, 'Informations de l\'étudiant mises à jour avec succès.')
            return redirect('student:student_detail', pk=pk)
    else:
        form = StudentUpdateForm(instance=student)
    
    return render(request, 'student/student_form.html', {'form': form, 'title': 'Modifier un étudiant'})

@login_required
def student_detail(request, pk):
    student = get_object_or_404(Student, pk=pk)
    academic_records = student.academic_records.all().order_by('-academic_year', '-semester')
    
    context = {
        'student': student,
        'academic_records': academic_records,
    }
    return render(request, 'student/student_detail.html', context)

@admin_required
def academic_record_create(request, student_pk):
    student = get_object_or_404(Student, pk=student_pk)
    if request.method == 'POST':
        form = AcademicRecordForm(request.POST)
        if form.is_valid():
            academic_record = form.save(commit=False)
            academic_record.student = student
            academic_record.save()
            messages.success(request, 'Dossier académique créé avec succès.')
            return redirect('student:student_detail', pk=student_pk)
    else:
        form = AcademicRecordForm()
    
    return render(request, 'student/academic_record_form.html', {
        'form': form,
        'student': student,
        'title': 'Créer un dossier académique'
    })

@admin_required
def academic_record_update(request, pk):
    academic_record = get_object_or_404(AcademicRecord, pk=pk)
    if request.method == 'POST':
        form = AcademicRecordForm(request.POST, instance=academic_record)
        if form.is_valid():
            form.save()
            messages.success(request, 'Dossier académique mis à jour avec succès.')
            return redirect('student:student_detail', pk=academic_record.student.pk)
    else:
        form = AcademicRecordForm(instance=academic_record)
    
    return render(request, 'student/academic_record_form.html', {
        'form': form,
        'student': academic_record.student,
        'title': 'Modifier le dossier académique'
    })

@student_required
def student_dashboard(request):
    student = get_object_or_404(Student, user=request.user)
    academic_records = student.academic_records.all().order_by('-academic_year', '-semester')
    
    context = {
        'student': student,
        'academic_records': academic_records,
    }
    return render(request, 'student/dashboard.html', context)
