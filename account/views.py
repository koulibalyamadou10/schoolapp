from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import User
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm
from .decorators import role_required

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)

            # Redirection selon rôle
            if user.role == 'admin':
                return redirect('admin_dashboard')
            elif user.role == 'teacher':
                return redirect('teacher_dashboard')
            elif user.role == 'student':
                return redirect('student_dashboard')
        else:
            messages.error(request, "Nom d'utilisateur ou mot de passe incorrect.")
            return render(request, 'account/login.html')

    return render(request, 'account/login.html')

@login_required
@role_required(['admin'])
def admin_dashboard(request):
    return render(request, 'account/admin_dashboard.html')

@login_required
@role_required(['teacher'])
def teacher_dashboard(request):
    return render(request, 'account/teacher_dashboard.html')

@login_required
@role_required(['student'])
def student_dashboard(request):
    return render(request, 'account/student_dashboard.html')

def register_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])  # Hachage du mot de passe
            user.save()
            return redirect('login')  # Redirige vers login après inscription
    else:
        form = UserRegistrationForm()
    return render(request, 'account/register.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')