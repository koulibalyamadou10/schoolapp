from django.urls import path

from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.teacher_dashboard, name='teacher_dashboard'),
    path('students/', views.students_by_class, name='teacher_students'),
    path('grades/', views.enter_grade, name='enter_grade'),
]
