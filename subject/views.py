from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from account.decorators import admin_required
from .models import Subject
from .forms import SubjectForm

@login_required
@admin_required
def subject_list(request):
    if request.method == 'POST':
        form = SubjectForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Matière ajoutée avec succès')
            return redirect('subject:subject_list')
    else:
        form = SubjectForm()
    
    subjects = Subject.objects.all().select_related('teacher')
    return render(request, 'subject/subject_list.html', {
        'form': form,
        'subjects': subjects
    })

@login_required
@admin_required
def edit_subject(request, subject_id):
    subject = get_object_or_404(Subject, id=subject_id)
    if request.method == 'POST':
        form = SubjectForm(request.POST, instance=subject)
        if form.is_valid():
            form.save()
            messages.success(request, 'Matière modifiée avec succès')
            return redirect('subject:subject_list')
    else:
        form = SubjectForm(instance=subject)
    
    return render(request, 'subject/edit_subject.html', {
        'form': form,
        'subject': subject
    })

@login_required
@admin_required
def delete_subject(request, subject_id):
    subject = get_object_or_404(Subject, id=subject_id)
    subject.delete()
    messages.success(request, 'Matière supprimée avec succès')
    return redirect('subject:subject_list')
