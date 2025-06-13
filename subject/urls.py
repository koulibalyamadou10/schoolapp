
from django.urls import path
from . import views

app_name = 'subject'

urlpatterns = [
    path('', views.subject_list, name='subject_list'),
    path('<int:subject_id>/edit/', views.edit_subject, name='edit_subject'),
    path('<int:subject_id>/delete/', views.delete_subject, name='delete_subject'),
]
