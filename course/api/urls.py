from django.urls import path
from . import views

urlpatterns = [
    path('', views.list_all_programs, name='list_all_programs'),
    path('program/<int:pk>/', views.get_program_by_id, name='get_program_by_id'),
    path('program_delete/<int:pk>/', views.get_or_delete_program, name='get_or_delete_program'),
     path('all_courses/', views.list_all_the_courses, name='list_all_the_courses'),
    path('create_course/', views.create_course, name='create_course'),
    path('course/<int:pk>/', views.get_course_by_id, name='get_course_by_id'),
    path('delete_course/<int:pk>/', views.delete_course, name='delete_course'),
]
