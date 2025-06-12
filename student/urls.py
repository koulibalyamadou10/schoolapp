
from django.urls import path
from . import views

app_name = 'student'

urlpatterns = [
    # Gestion des étudiants
    path('list/', views.student_list, name='student_list'),
    path('create/', views.student_create, name='student_create'),
    path('<int:pk>/', views.student_detail, name='student_detail'),
    path('<int:pk>/update/', views.student_update, name='student_update'),
    
    # Gestion des dossiers académiques
    path('<int:student_pk>/academic-record/create/',
         views.academic_record_create, name='academic_record_create'),
    path('academic-record/<int:pk>/update/',
         views.academic_record_update, name='academic_record_update'),
    
    # Tableau de bord étudiant
    path('dashboard/', views.student_dashboard, name='dashboard'),
]
