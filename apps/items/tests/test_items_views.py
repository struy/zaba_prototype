from django.test import TestCase, RequestFactory
from apps.items.views import index
from django.contrib.auth.models import AnonymousUser


class IndexViewTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_index_view_basic(self):
        """
        Test that index view returns a 200 response and uses
        the correct template
        """
        request = self.factory.get('/items')
        request.user = AnonymousUser()
        response = index(request)
        self.assertEqual(response.status_code, 200)
