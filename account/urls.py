from django.urls import path
from .views import (
    login_view, register_view, logout_view,
    admin_dashboard, profile_view, change_password_view,
    password_reset_view, password_reset_confirm_view,
    unauthorized_view
)

app_name = 'account'

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
    path('admin-dashboard/', admin_dashboard, name='dashboard'),
    
    # Error Pages
    path('unauthorized/', unauthorized_view, name='unauthorized'),
]