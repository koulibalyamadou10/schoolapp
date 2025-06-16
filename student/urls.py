from django.urls import path
from . import views

app_name = 'student'

urlpatterns = [
    # Gestion des étudiants
    path('list/', views.student_list, name='student-list'),
    path('create/', views.student_create, name='student-create'),
    path('<int:pk>/detail/', views.student_detail, name='student-detail'),
    path('<int:pk>/update/', views.student_update, name='student-update'),
    
    # Gestion des dossiers académiques
    path('<int:student_pk>/academic-record/create/',
         views.academic_record_create, name='academic-record-create'),
    path('academic-record/<int:pk>/update/',
         views.academic_record_update, name='academic-record-update'),
    
    # Tableau de bord étudiant
    path('dashboard/', views.student_dashboard, name='dashboard'),
    
    # Notes et emploi du temps
    path('mes-notes/', views.student_grades, name='student-grades'),
    path('schedule/', views.student_schedule, name='student-schedule'),

    # Export PDF
    path('<int:pk>/export-pdf/', views.export_academic_report_pdf, name='export-academic-report-pdf'),
    path('my-report-pdf/', views.export_my_academic_report_pdf, name='export-my-academic-report-pdf'),

    path('unauthorized/', views.unauthorized_view, name='unauthorized'),
]