from django.test import TestCase, RequestFactory
from apps.sendemail.views import contact_view
from django.contrib.auth.models import AnonymousUser


class IndexViewTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_index_view_basic(self):
        """
        Test that index view returns a 200 response and uses
        the correct template
        """
        request = self.factory.get('/contact')
        request.user = AnonymousUser()
        response = contact_view(request)
        self.assertEqual(response.status_code, 200)
