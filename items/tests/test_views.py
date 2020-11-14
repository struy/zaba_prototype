from django.test import RequestFactory
from django.urls import reverse
from django.contrib.auth.models import User, AnonymousUser
from items.views import ItemCreate
from mixer.backend.django import mixer
import pytest

from items.views import index


@pytest.mark.django_db
def test_items_index(rf):
    request = rf.get('/items/')
    response = index(request)
    assert response.status_code == 200

# @pytest.mark.django_db
# def test_view(client):
#     url = reverse('items:index')
#     response = client.get(url)
#     assert response.status_code == 200


# @pytest.mark.django_db
# def test_superuser_view(admin_client):
#     url = reverse('items:index')
#     response = admin_client.get(url)
#     assert response.status_code == 200

# @pytest.mark.django_db
# def test_item_create_authenticated(client):
#     path = reverse('items:new')
#     request = RequestFactory().get(path)
#     request.user = mixer.blend(User)
#     response = client.get(path)
#     assert response.status_code == 200
#
#
# @pytest.mark.django_db
# def test_item_create_unauthenticated(client):
#     path = reverse('items:new')
#     request = RequestFactory().get(path)
#     request.user = AnonymousUser()
#     response = client.get(path)
#     assert response.status_code == 302
#     assert 'accounts/login' in response.url
