from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.messages import get_messages

class HomeViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.home_url = reverse('home')

    def test_get_request(self):
        response = self.client.get(self.home_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')

    def test_post_request_valid_credentials(self):
        # Create a test user
        user = User.objects.create_user(username='testuser', password='testpassword')
        # Post request with valid credentials
        response = self.client.post(self.home_url, {'username': 'testuser', 'password': 'testpassword'})
        self.assertEqual(response.status_code, 302)
        # Check if user is logged in
        self.assertTrue('_auth_user_id' in self.client.session)
        # Check success message
        messages = [m.message for m in get_messages(response.wsgi_request)]
        self.assertIn("You Have Been Logged In!", messages)

    def test_post_request_invalid_credentials(self):
        # Post request with invalid credentials
        response = self.client.post(self.home_url, {'username': 'invaliduser', 'password': 'invalidpassword'})
        self.assertEqual(response.status_code, 302)
        # Check if user is not logged in
        self.assertFalse('_auth_user_id' in self.client.session)
        # Check error message
        messages = [m.message for m in get_messages(response.wsgi_request)]
        self.assertIn("There Was An Error Logging In, Please Try Again...", messages)
