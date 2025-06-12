# account/decorators.py
from django.shortcuts import redirect
from functools import wraps

def role_required(allowed_roles):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if request.user.is_authenticated and request.user.role in allowed_roles:
                return view_func(request, *args, **kwargs)
            if not request.user.is_authenticated:
                return redirect('account:login')
            return redirect('account:unauthorized')  # Redirection vers notre page 401
        return wrapper
    return decorator

# Décorateurs spécifiques pour chaque rôle
def admin_required(view_func):
    return role_required(['admin'])(view_func)

def teacher_required(view_func):
    return role_required(['teacher'])(view_func)

def student_required(view_func):
    return role_required(['student'])(view_func)
