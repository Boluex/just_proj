from django.urls import reverse
from rest_framework.test import APITestCase

from accounts.models import User,Student
from .views import list_users

class UserViewTest(APITestCase):

    def test_list_users(self):
        url = reverse('list_users')

        # Create some sample users
        User.objects.create_user(username='lecturer', email='lecturer@email.com',is_lecturer=True)
        User.objects.create_user(username='student', email='student@email.com',is_student=True)

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)  # Verify number of users returned


class StudentViewTest(APITestCase):

    def test_list_students(self):
        url = reverse('list_students')

        # Create some sample students
        student1 = Student.objects.create(student=User.objects.create_user(username='student1'), level='Level 1')
        student2 = Student.objects.create(student=User.objects.create_user(username='student2'), level='Level 2')

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)  # Verify number of students returned
