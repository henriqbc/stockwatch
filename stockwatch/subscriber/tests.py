from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse

class SubscriberViewsTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_subscribe_get(self):
        response = self.client.get(reverse('subscriber:subscribe'))
        
        self.assertEqual(response.status_code, 200)

    def test_subscribe_post(self):
        data = {'name': 'Test User', 'email': 'test@example.com'}
        response = self.client.post(reverse('subscriber:subscribe'), data)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('subscriber:home'))

    def test_user_home_redirect_when_unsubscribed(self):
        response = self.client.get(reverse('subscriber:home'))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('subscriber:subscribe'))

    def test_user_reset_as_superuser(self):
        admin = User.objects.create_superuser(username='sw-admin', email='', password='sw-password')
        self.client.login(username='sw-admin', password='sw-password')

        response = self.client.get(reverse('subscriber:reset'))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('subscriber:subscribe'))

    def test_user_reset_as_not_superuser(self):
        response = self.client.get(reverse('subscriber:reset'))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/server-error/')
