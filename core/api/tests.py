from django.urls import reverse
from rest_framework.test import APITestCase

from core.models import Session,NewsAndEvents
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


#########################################
# session test
#########################################
class SessionViewTest(APITestCase):

    def setUp(self):
        self.session_data = {
            'session': 'Test Session',
            'next_session_begins': '2024-03-15',  # Example date
        }

    def test_create_session_valid(self):
        url = reverse('create_session')
        self.client.login(username='admin', password='admin123')

        response = self.client.post(url, data=self.session_data, format='json')

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['session'], self.session_data['session'])

    def test_create_session_invalid_data(self):
        url = reverse('create_session')
        self.client.login(username='admin', password='admin123')

        data = {}  # Missing required fields
        response = self.client.post(url, data=data, format='json')

        self.assertEqual(response.status_code, 400)

    def test_list_sessions(self):
        url = reverse('list_sessions')

        # Create a sample session
        Session.objects.create(**self.session_data)

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)  # Verify number of objects returned

    def test_get_session_by_name_valid(self):
        session = Session.objects.create(**self.session_data)
        url = reverse('get_session_by_name', kwargs={'name': session.session})

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['session'], session.session)

    def test_get_session_by_name_invalid(self):
        url = reverse('get_session_by_name', kwargs={'name': 'Non-existent Session'})

        response = self.client.get(url)

        self.assertEqual(response.status_code, 404)

    def test_update_session_valid(self):
        session = Session.objects.create(**self.session_data)
        url = reverse('update_session', kwargs={'name': session.session})

        data = {
            'next_session_begins': '2025-01-01',  # Update start date
        }

        self.client.login(username='admin', password='admin123')
        response = self.client.put(url, data=data, format='json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['next_session_begins'], data['next_session_begins'])

    def test_update_session_invalid_data(self):
        session = Session.objects.create(**self.session_data)
        url = reverse('update_session', kwargs={'name': session.session})

        data = {}  # No update data
        self.client.login(username='admin', password='admin123')
        response = self.client.put(url, data=data, format='json')

        self.assertEqual(response.status_code, 400)

    def test_delete_session_valid(self):
        session = Session.objects.create(**self.session_data)
        url = reverse('delete_session', kwargs={'name': session.session})

        self.client.login(username='admin', password='admin123')
        response = self.client.delete(url)

        self.assertEqual(response.status_code, 204)

#########################################
# news and event test
#########################################
class NewsAndEventsViewTest(APITestCase):

    def setUp(self):
        self.news_data = {
            'title': 'Test News',
            'summary': 'This is a test news article.',
            'posted_as': 'News',
        }
        self.event_data = {
            'title': 'Test Event',
            'summary': 'This is a test event.',
            'posted_as': 'Events',
        }

    # Test creating a new news
    def test_create_news_valid(self):
        url = reverse('list_news_and_events')
        self.client.login(username='admin', password='admin123')

        response = self.client.post(url, data=self.news_data, format='json')

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['title'], self.news_data['title'])

    # Test creating a new event (similar pattern)
    def test_create_event_valid(self):
        url = reverse('list_news_and_events')
        self.client.login(username='admin', password='admin123')

        response = self.client.post(url, data=self.event_data, format='json')

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['title'], self.event_data['title'])

    # Test creating news with invalid data
    def test_create_news_invalid_data(self):
        url = reverse('list_news_and_events')
        self.client.login(username='admin', password='admin123')

        data = {}  # Missing required fields
        response = self.client.post(url, data=data, format='json')

        self.assertEqual(response.status_code, 400)

    # Test retrieving all news and events
    def test_list_news_and_events(self):
        url = reverse('list_news_and_events')

        # Create some sample news and events
        NewsAndEvents.objects.create(**self.news_data)
        NewsAndEvents.objects.create(**self.event_data)

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)  # Verify number of objects returned

    # Test retrieving news or event by ID (valid and invalid)
    def test_get_news_or_event_by_id_valid(self):
        news_obj = NewsAndEvents.objects.create(**self.news_data)
        url = reverse('get_news_or_event_by_id', kwargs={'pk': news_obj.pk})

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['title'], news_obj.title)

    def test_get_news_or_event_by_id_invalid(self):
        url = reverse('get_news_or_event_by_id', kwargs={'pk': 1000})  # Non-existent ID

        response = self.client.get(url)

        self.assertEqual(response.status_code, 404)
 
    # Test deleting news or event (similar pattern to retrieval)
    def test_delete_news_valid(self):
        news_obj = NewsAndEvents.objects.create(**self.news_data)
        url = reverse('delete_news_or_event', kwargs={'pk': news_obj.pk})
        self.client.login(username='admin', password='admin123')

        response = self.client.delete(url)

        self.assertEqual(response.status_code, 204)  # No content returned

    def test_delete_news_invalid(self):
        url = reverse('delete_news_or_event', kwargs={'pk': 1000})  # Non-existent ID
        self.client.login(username='admin', password='admin123')

        response = self.client.delete(url)

        self.assertEqual(response.status_code, 404)

