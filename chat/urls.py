from django.urls import path
from.import views


urlpatterns=[
    path('filter_messages/',views.filter_messages,name='filter_messages'),
    path('active_lecturers/',views.all_active_users,name='active_users'),
    path('<str:username>/',views.home,name='room'),
]