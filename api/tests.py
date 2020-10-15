from django.test import TestCase


class HomePageTest(TestCase):

    def test_uses_home_template(self):
        response = self.client.get('/api/simulations/')
        self.assertEqual(response.status_code, 200)

