from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Subject
from .forms import SubjectForm

def subject_list(request):
    subjects = Subject.objects.select_related('teacher').all()
    return render(request, 'subject/subject_list.html', {'subjects': subjects})

def subject_create(request):
    if request.method == 'POST':
        form = SubjectForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Matière créée avec succès.")
            return redirect('subject_list')
    else:
        form = SubjectForm()
    return render(request, 'subject/subject_form.html', {'form': form})

def subject_update(request, pk):
    subject = get_object_or_404(Subject, pk=pk)
    if request.method == 'POST':
        form = SubjectForm(request.POST, instance=subject)
        if form.is_valid():
            form.save()
            messages.success(request, "Matière modifiée avec succès.")
            return redirect('subject_list')
    else:
        form = SubjectForm(instance=subject)
    return render(request, 'subject/subject_form.html', {'form': form})

def subject_delete(request, pk):
    subject = get_object_or_404(Subject, pk=pk)
    if request.method == 'POST':
        subject.delete()
        messages.success(request, "Matière supprimée avec succès.")
        return redirect('subject_list')
    return render(request, 'subject/subject_confirm_delete.html', {'subject': subject})