# account/decorators.py
from django.shortcuts import redirect
from functools import wraps

def role_required(allowed_roles):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if request.user.is_authenticated and request.user.role in allowed_roles:
                return view_func(request, *args, **kwargs)
            return redirect('login')  # ou créer une page '403'
        return wrapper
    return decorator
