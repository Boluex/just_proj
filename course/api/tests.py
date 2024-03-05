from django.urls import reverse  # Import for generating URLs
from rest_framework.test import APITestCase
from rest_framework import status
from course.models import Program,Course
from course.api.views import list_all_programs
from .views import create_course

class AllProgramsViewTest(APITestCase):
    def setUp(self):
        self.program1 = Program.objects.create(title="Program 1", summary="Summary 1")
        self.program2 = Program.objects.create(title="Program 2", summary="Summary 2")

    def test_list_all_programs_authenticated(self):
        url = reverse('list_all_programs')  

        self.client.login(username='admin', password='admin123')

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2) 


    def test_list_all_programs_unauthenticated(self):
        url = reverse('list_all_programs')  

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED) 



class GetProgramByIdViewTest(APITestCase):

    def test_get_program_by_id(self):
        program = Program.objects.create(title="Program 1", summary="Summary 1")
        url = reverse('get_program_by_id', kwargs={'pk': program.pk})
        self.client.login(username='admin', password='admin123')

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'title': program.title, 'summary': program.summary})

    def test_get_program_by_id_not_found(self):
        url = reverse('get_program_by_id', kwargs={'pk': 100})  

        self.client.login(username='admin', password='admin123')

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)




from .views import get_or_delete_program

class GetOrDeleteProgramViewTest(APITestCase):
    def setUp(self):
        self.program = Program.objects.create(title="Program 1", summary="Summary 1")

    def test_get_program_by_id(self):
        url = reverse('get_or_delete_program', kwargs={'pk': self.program.pk})

        self.client.login(username='admin', password='admin123')

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'title': self.program.title, 'summary': self.program.summary})

    def test_get_program_by_id_not_found(self):
        url = reverse('get_or_delete_program', kwargs={'pk': 100})  

        self.client.login(username='admin', password='admin123')

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_program(self):
        url = reverse('get_or_delete_program', kwargs={'pk': self.program.pk})

        # Authenticate the user (if authentication is enforced)
        self.client.login(username='valid_user', password='valid_password')

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Check if the program is actually deleted
        self.assertFalse(Program.objects.filter(pk=self.program.pk).exists())





class CreateCourseViewTest(APITestCase):
    def setUp(self):
        self.program = Program.objects.create(title="Test Program")

    def test_create_course_valid(self):
        url = reverse('create_course')
        self.client.login(username='admin', password='admin123')

        data = {
            'slug': 'test-course',
            'title': 'Test Course',
            'code': 'TEST101',
            'credit': 30,
            'summary': 'This is a test course.',
            'program': self.program.pk,
            'level':'Bachelor',
            'year': 2024,
            'semester': 'First',
        }

        response = self.client.post(url, data=data, format='json')

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['program'], self.program.pk)  # Verify program association
        self.assertEqual(response.data['title'], data['title'])

        created_course = Course.objects.get(pk=response.data['id'])
        self.assertEqual(created_course.program, self.program)

    def test_create_course_invalid_data(self):
        url = reverse('create_course')

        # Authenticate the user (if authentication is enforced)
        self.client.login(username='valid_user', password='valid_password')

        data = {
            'title': 'Test Course',  # Missing required fields
        }

        response = self.client.post(url, data=data, format='json')

        self.assertEqual(response.status_code, 400)

    def test_create_course_invalid_program(self):
        url = reverse('create_course')

        # Authenticate the user (if authentication is enforced)
        self.client.login(username='valid_user', password='valid_password')

        data = {
            'slug': 'test-course',
            'title': 'Test Course',
            'code': 'TEST101',
            'credit': 3,
            'summary': 'This is a test course.',
            'program': 100,  # Invalid program ID
            'level': 'Bachelor',
            'year': 2024,
            'semester': 'First',
        }

        response = self.client.post(url, data=data, format='json')

        self.assertEqual(response.status_code, 400)  # Expect 400 for invalid program