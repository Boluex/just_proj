from django.urls import path
from .views import (
    create_news_or_event,
    list_news_and_events,
    get_news_or_event_by_id,
    delete_news_or_event,
    create_session,
    list_sessions,
    get_session_by_name,
    update_session,
    delete_session,
)

urlpatterns = [
    # The news and event urls
    path('', list_news_and_events, name='list_news_and_events'),
    path('create_news/',create_news_or_event,name='create_news_or_event'),
    path('get_news/',get_news_or_event_by_id,name='get_news_or_event_by_id'),
    path('delete_news/',delete_news_or_event,name='delete_news_or_event'),
    # The session urls

    path('session/', list_sessions, name='list_sessions'),
    path('create_session/', create_session, name='create_session'),
    path('detail_session/<str:name>/', get_session_by_name, name='get_session_by_name'),
    path('update_session/<str:name>/', update_session, name='update_session'),
    path('delete_session/<str:name>/',delete_session,name='delete_session'),
]


   
    