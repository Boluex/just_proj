from django.urls import path
from .views import list_users, get_user_by_id,create_user,update_user,delete_user,list_students,get_student_by_id,update_student,delete_student,create_student

urlpatterns = [
                    # users urls
                    path('', list_users, name='list_users'),
                    path('get_user/<int:pk>/', get_user_by_id, name='get_user_by_id'),
                    path('create_user/',create_user,name='create_user'),
                    path('update_user/<int:pk>',update_user,name='update_user'),
                    path('delete_user/<int:pk>/',delete_user,name='delete_user'),



                    # student urls
                    path('student/', list_students, name='list_students'),
                    path('get_student/<int:pk>/', get_student_by_id, name='get_student_by_id'),
                    path('create_student/',create_student,name='create_student'),
                    path('update_student/<int:pk>',update_student,name='update_student'),
                    path('delete_student/<int:pk>/',delete_student,name='delete_student')
                ]    