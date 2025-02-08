from django.test import TestCase, Client
from django.urls import reverse

class StockwatchAppTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_homepage(self):
        response = self.client.get(reverse('homepage'))

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Stockwatch", response.content)

    def test_server_error_page(self):
        response = self.client.get(reverse('server-error'))

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Oh, no!", response.content)

    def test_navbar_links(self):
        response = self.client.get(reverse('homepage'))

        self.assertEqual(response.status_code, 200)
        
        content = response.content.decode('utf-8')

        self.assertIn("home", content)
        self.assertIn("stocks/", content)
        self.assertIn("user/", content)
