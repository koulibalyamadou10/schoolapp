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
from django.urls import reverse
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
            if user.role == 'admin':
                return redirect('account:dashboard')
            elif user.role == 'teacher':
                return redirect('teacher:dashboard')
            else:
                return redirect('student:dashboard')
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
            })
            
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
    return render(request, 'account/admin_dashbord.html')

    