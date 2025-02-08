from django.test import TestCase, Client
from django.urls import reverse

class StocksViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.subscription_data = {'name': 'Stock User', 'email': 'user@example.com'}

    def subscribe_user_helper(self):
        self.client.post(reverse('subscriber:subscribe'), self.subscription_data)

    def test_clear_stock_list_unsubscribed(self):
        response = self.client.get(reverse('stocks:full-delete'))

        self.assertRedirects(response, reverse('stocks:home'))

    def test_stocks_new_unsubscribed(self):
        response = self.client.get(reverse('stocks:new'))

        self.assertRedirects(response, reverse('stocks:home'))
    
    def test_stock_page_unsubscribed(self):
        response = self.client.post(reverse('stocks:page', kwargs={'name': 'TEST'}))

        self.assertRedirects(response, reverse('stocks:home'))

    def test_stock_update_unsubscribed(self):
        response = self.client.post(reverse('stocks:update', kwargs={'name': 'TEST'}))

        self.assertRedirects(response, reverse('stocks:home'))

    def test_stock_delete_unsubscribed(self):
        response = self.client.get(reverse('stocks:delete', kwargs={'name': 'TEST'}))

        self.assertRedirects(response, reverse('stocks:home'))
 
    def test_stock_full_delete_unsubscribed(self):
        response = self.client.get(reverse('stocks:full-delete'))

        self.assertRedirects(response, reverse('stocks:home'))

    def test_add_stock_success(self):
        self.subscribe_user_helper()
        stock_data = {
            'name': 'VALE3',
            'periodicity': 15,
            'upper_tunnel_bound': 150,
            'lower_tunnel_bound': 140,
        }
        
        response = self.client.post(reverse('stocks:new'), stock_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('stocks:list'))

    def test_add_invalid_stock(self):
        self.subscribe_user_helper()
        stock_data = {
            'name': 'TEST',
            'periodicity': 15,
            'upper_tunnel_bound': 150,
            'lower_tunnel_bound': 140,
        }

        response = self.client.post(reverse('stocks:new'), stock_data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'stocks/new_stock.html')

    def test_invalid_stock_name_redirect(self):
        self.subscribe_user_helper()
        
        response = self.client.get(reverse('stocks:page', kwargs={'name': 'TEST'}))

        self.assertRedirects(response, reverse('stocks:new'))

    def test_update_stock(self):
        self.subscribe_user_helper()

        stock_data = {
            'name': 'VALE3',
            'periodicity': 15,
            'upper_tunnel_bound': 150,
            'lower_tunnel_bound': 140,
        }
 
        response = self.client.post(reverse('stocks:new'), data=stock_data)

        update_data = {
            'periodicity': 30,
            'upper_tunnel_bound': 155,
            'lower_tunnel_bound': 135,
        }

        response = self.client.post(reverse('stocks:update', kwargs={'name': 'TEST'}), date=update_data, follow=True)

        self.assertRedirects(response, reverse('stocks:list'))

    def test_update_stock_not_registered(self):
        self.subscribe_user_helper()

        update_data = {
            'periodicity': 30,
            'upper_tunnel_bound': 155.0,
            'lower_tunnel_bound': 135.0,
        }

        response = self.client.post(reverse('stocks:update', kwargs={'name': 'TEST'}), update_data, follow=True)

        self.assertRedirects(response, reverse('stocks:new'))

    def test_delete_stock(self):
        self.subscribe_user_helper()
        stock_data = {
            'name': 'VALE3',
            'periodicity': 15,
            'upper_tunnel_bound': 150,
            'lower_tunnel_bound': 140,
        }
        
        self.client.post(reverse('stocks:new'), stock_data)

        response = self.client.get(reverse('stocks:delete', kwargs={'name': 'VALE3'}), follow=True)

        self.assertRedirects(response, reverse('stocks:new'))
    
    def test_delete_stock_not_registered(self):
        self.subscribe_user_helper()
        response = self.client.get(reverse('stocks:delete', kwargs={'name': 'VALE3'}))

        self.assertRedirects(response, reverse('server-error'))

    def test_clear_stock_list(self):
        self.subscribe_user_helper()
        stock_data = {
            'name': 'VALE3',
            'periodicity': 15,
            'upper_tunnel_bound': 150,
            'lower_tunnel_bound': 140,
        }

        self.client.post(reverse('stocks:new'), stock_data)

        response = self.client.get(reverse('stocks:full-delete'))

        self.assertRedirects(response, reverse('stocks:new'))