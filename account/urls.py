from django.urls import path
from .views import (
    login_view, register_view, logout_view,
    admin_dashboard, teacher_dashboard, student_dashboard,
    profile_view, change_password_view,
    password_reset_view, password_reset_confirm_view
)

urlpatterns = [
    # Authentication URLs
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('logout/', logout_view, name='logout'),
    
    # Profile Management URLs
    path('profile/', profile_view, name='profile'),
    path('profile/change-password/', change_password_view, name='change_password'),
    
    # Password Reset URLs
    path('password-reset/', password_reset_view, name='password_reset'),
    path('password-reset-confirm/<str:uidb64>/<str:token>/',
         password_reset_confirm_view, name='password_reset_confirm'),
    
    # Dashboard URLs
    path('admin-dashboard/', admin_dashboard, name='admin_dashboard'),
    path('teacher-dashboard/', teacher_dashboard, name='teacher_dashboard'),
    path('student-dashboard/', student_dashboard, name='student_dashboard'),
]