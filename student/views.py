from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Student, AcademicRecord
from .forms import StudentCreationForm, StudentRegistrationForm, StudentUpdateForm, AcademicRecordForm
from .utils import create_pdf_response
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


def unauthorized_view(request, exception=None):
    return render(request, '401.html', status=401)

@admin_required
def student_create(request):
    if request.method == 'POST':
        form = StudentCreationForm(request.POST)
        if form.is_valid():
            try:
                student = form.save()
                messages.success(
                    request, 
                    'Étudiant créé avec succès. Un email avec les identifiants de connexion a été envoyé.'
                )
                return redirect('student:student-detail', pk=student.pk)
            except Exception as e:
                messages.error(
                    request,
                    "Une erreur s'est produite lors de la création de l'étudiant. Veuillez réessayer."
                )
                print(f"Erreur lors de la création de l'étudiant : {e}")
    else:
        form = StudentCreationForm()
    
    context = {
        'form': form,
        'title': 'Créer un étudiant',
        'form_errors': form.errors if request.method == 'POST' else None
    }
    return render(request, 'student/student_form.html', context)

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
    try:
        student = get_object_or_404(Student, pk=student_pk)
        if request.method == 'POST':
            form = AcademicRecordForm(request.POST)
            if form.is_valid():
                academic_record = form.save(commit=False)
                academic_record.student = student
                academic_record.save()
                messages.success(request, 'Dossier académique créé avec succès.')
                return redirect('student:student-detail', pk=student_pk)
        else:
            form = AcademicRecordForm()

        return render(request, 'student/academic_record_form.html', {
            'form': form,
            'student': student,
            'title': 'Créer un dossier académique'
        })
    except Exception as e:
        return HttpResponse(e)


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
def student_grades(request):
    # Récupérer l'étudiant connecté
    student = get_object_or_404(Student, user=request.user)
    # Récupérer tous les dossiers académiques de l'étudiant
    academic_records = student.academic_records.all().order_by('-academic_year', '-semester')
    # Récupérer toutes les notes individuelles de l'étudiant
    from grade.models import Grade
    from django.db.models import Avg
    grades = Grade.objects.filter(student=student).select_related('subject').order_by('-date')
    
    # Calculer la moyenne générale de toutes les notes
    overall_average = grades.aggregate(avg_grade=Avg('grade'))['avg_grade']
    if overall_average:
        overall_average = round(overall_average, 2)
    
    context = {
        'student': student,
        'academic_records': academic_records,
        'grades': grades,
        'overall_average': overall_average,
    }
    return render(request, 'student/student_grades.html', context)

@student_required
def student_schedule(request):
    # Récupérer l'étudiant connecté
    student = get_object_or_404(Student, user=request.user)
    # Vous devrez ajouter la logique pour récupérer l'emploi du temps
    # en fonction de la classe de l'étudiant
    
    context = {
        'student': student,
        # 'schedule': schedule,  # À implémenter selon votre modèle d'emploi du temps
    }
    return render(request, 'student/student_schedule.html', context)

@student_required
def student_dashboard(request):
    student = get_object_or_404(Student, user=request.user)
    academic_records = student.academic_records.all().order_by('-academic_year', '-semester')
    
    context = {
        'student': student,
        'academic_records': academic_records,
    }
    return render(request, 'account/student_dashboard.html', context)

@login_required
def export_academic_report_pdf(request, pk):
    """
    Exporte le bulletin de notes d'un étudiant au format PDF
    """
    student = get_object_or_404(Student, pk=pk)
    
    # Vérifier les permissions
    if request.user.role == 'student' and student.user != request.user:
        messages.error(request, "Vous n'avez pas l'autorisation d'accéder à ce bulletin.")
        return redirect('student:unauthorized')
    elif request.user.role not in ['admin', 'teacher', 'student']:
        messages.error(request, "Vous n'avez pas l'autorisation d'accéder à cette fonctionnalité.")
        return redirect('student:unauthorized')
    
    # Récupérer les données
    academic_records = student.academic_records.all().order_by('-academic_year', '-semester')
    
    # Récupérer les notes individuelles si disponibles
    from grade.models import Grade
    grades = Grade.objects.filter(student=student).select_related('subject').order_by('subject__name', '-date')
    
    # Générer et retourner le PDF
    try:
        return create_pdf_response(student, academic_records, grades)
    except Exception as e:
        messages.error(request, f"Erreur lors de la génération du PDF : {str(e)}")
        return redirect('student:student-detail', pk=pk)

@login_required
def export_my_academic_report_pdf(request):
    """
    Permet à un étudiant d'exporter son propre bulletin de notes
    """
    if request.user.role != 'student':
        messages.error(request, "Cette fonctionnalité est réservée aux étudiants.")
        return redirect('account:dashboard')
    
    student = get_object_or_404(Student, user=request.user)
    return export_academic_report_pdf(request, student.pk)