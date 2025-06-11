from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # --- URLs CRUD UTILISATEURS ---
    path('users/', views.user_list, name='user_list'),
    path('users/create/', views.user_create, name='user_create'),
    path('users/<int:pk>/edit/', views.user_update, name='user_update'),
    path('users/<int:pk>/delete/', views.user_delete, name='user_delete'),

    # --- URL TABLEAU DE BORD ADMIN ---
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    
    # --- URL CONNEXION ---
    path('login/', auth_views.LoginView.as_view(template_name='account/login.html'), name='login'),
    
    # --- URL pour les statistiques des notes ---
    path('grades-stats/', views.admin_grades_stats, name='admin_grades_stats'),
]