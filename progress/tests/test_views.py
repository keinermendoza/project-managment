from django.test import TestCase, Client, RequestFactory
from django.urls import reverse
from account.models import User
from progress.models import Project, Task
from progress.views import project_detail, projects_all\
, projects_private, projects_public, admin_project_view

class TestProjectViews(TestCase):
    def setUp(self):
        
        self.requestFactory = RequestFactory()
        self.client = Client()

        # creating users
        data_user_one = {
            'username': 'User one',
            'email': 'iliketodoprojects@gmail.com',
            'password': 'password'
        }
        data_user_two = {
            'username': 'User two',
            'email': 'imatwouser@gmail.com',
            'password': 'password'
        }
        data_user_admin = {
            'username': 'ADMIN',
            'email': 'superadmin@gmail.com',
            'password': 'admin_password',
            'is_staff': True,
            'is_superuser': True
        }

        self.user_one = User.objects.create(**data_user_one)        
        self.user_two = User.objects.create(**data_user_two)        
        self.user_admin = User.objects.create(**data_user_admin)        

        # creating projects
        data_public_project_1 = {
            'user': self.user_one,
            'name': 'public project',
            'description': 'description of my test project',
        }

        data_private_project_1 = {
            'user': self.user_one,
            'public': False,
            'name': 'public project',
            'description': 'description of my test project',
        }

        data_private_project_2 = {
            'user': self.user_one,
            'public': False,
            'name': 'public project',
            'description': 'description of my test project',
        }
        self.public_project_1 = Project.objects.create(**data_public_project_1)
        self.private_project_1 = Project.objects.create(**data_private_project_1)
        self.private_project_2 = Project.objects.create(**data_private_project_2)

        self.routes = {
            'home': reverse('progress:projects_home'),
            'all': reverse('progress:projects_all'),
            'public': reverse('progress:projects_public'),
            'private': reverse('progress:projects_private'),
            'detail_public_1': reverse('progress:project_detail', args=[self.public_project_1.id]),
            'detail_private_1': reverse('progress:project_detail', args=[self.private_project_1.id]),
            'detail_private_2"': reverse('progress:project_detail', args=[self.private_project_2.id]),
            'admin_view': reverse('progress:admin_project_view', args=[self.private_project_1.id]),
        }

        self.use_HTMX = {'HTTP_HX-Request': 'true'}
        
        # the request_factory is giving me and error so i used this for avoid it
        self.DONT_use_HTMX = {'HTTP_HX-Request': 'false'}


    def test_configuration(self):
        """checks the setUp is correct"""
        self.assertIsInstance(self.user_one, User)
        self.assertIsInstance(self.user_two, User)
        self.assertIsInstance(self.user_admin, User)
        self.assertTrue(self.user_admin.is_superuser)

        self.assertIsInstance(self.public_project_1, Project)
        self.assertIsInstance(self.private_project_1, Project)
        self.assertIsInstance(self.private_project_2, Project)

    ### TESTING VIEWS WITH AN ANONIMOUS USER
    def test_user_anonimous_get_home(self):
        """anonimous user can requests the home view"""
        
        response = self.client.get(self.routes['home'])
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'progress/base.html')
        self.assertTemplateUsed(response, 'progress/home.html')

    def test_user_anonimous_get_home_using_HTMX(self):
        """anonimous user can requests the home view USING HTMX
        the response is a partial html"""

        response = self.client.get(self.routes['home'], **self.use_HTMX)

        self.assertEqual(response.status_code, 200)
        self.assertNotIn('progress/base.html', response.templates)
        self.assertTemplateUsed(response, 'progress/snippets/home.html')

    def test_user_anonimous_get_projects_all(self):
        """anonimous user can requests the projects_all view
        response contains only the public projects"""
        
        response = self.client.get(self.routes['all'])

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'progress/project_list.html')
        self.assertIn(self.public_project_1, response.context['projects'])
        self.assertNotIn(self.private_project_1, response.context['projects'])

    def test_user_anonimous_get_projects_all_using_HTMX(self):
        """anonimous user can requests the projects_all view
        response contains only the public projects
        the response is a partial html"""
        
        response = self.client.get(self.routes['all'], **self.use_HTMX)
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'progress/snippets/project_list.html')
        self.assertNotIn('progress/base.html', response.templates)

        self.assertIn(self.public_project_1, response.context['projects'])
        self.assertNotIn(self.private_project_1, response.context['projects'])


    def test_user_one_get_get_projects_all(self):
        request = self.requestFactory.get(self.routes['all'])
        request.user = self.user_one
        response = projects_all(request)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'progress/project_list.html')
        self.assertIn(self.public_project_1, response.context['projects'])

        # it's also present the private project of the current user
        self.assertIn(self.private_project_1, response.context['projects'])

        # self.assertNotIn(self.private_project_1, response.context['projects'])


    # def test_user_anonimous_get_projects_public_using_HTMX(self):
    #     """anonimous user can requests the projects_public view
    #     response contains only the public projects
    #     the response is a partial html"""
        
    #     response = self.client.get(self.routes['public'], **self.use_HTMX)
        
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTemplateUsed(response, 'progress/snippets/project_list.html')
    #     self.assertNotIn('progress/base.html', response.templates)

    #     self.assertIn(self.public_project_1, response.context['projects'])
    #     self.assertNotIn(self.private_project_1, response.context['projects'])

    # def test_user_anonimous_get_projects_public_using_HTMX(self):
    #     """anonimous user can requests the projects_public view
    #     response contains only the public projects
    #     the response is a partial html"""
        
    #     response = self.client.get(self.routes['public'], **self.use_HTMX)
        
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTemplateUsed(response, 'progress/snippets/project_list.html')
    #     self.assertNotIn('progress/base.html', response.templates)

    #     self.assertIn(self.public_project_1, response.context['projects'])
    #     self.assertNotIn(self.private_project_1, response.context['projects'])


