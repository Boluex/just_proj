from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from accounts.models import User
from course.models import Program
from core.models import NewsAndEvents

class YourTestCase(APITestCase):
    
    def test_list_all_programs(self):
        url = reverse('list_all_programs')  

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED) 


    def test_all_course(self):
        url = reverse('list_all_the_courses')  

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED) 
