import pytest
from django.urls import reverse
from django.utils.translation import activate


@pytest.fixture()
def set_default_language():
    activate('en')


def test_an_admin_view(admin_client):
    response = admin_client.get('/admin/')
    assert response.status_code == 200


def test_with_authenticated_client(client, django_user_model):
    username = "user1"
    password = "bar"
    user = django_user_model.objects.create_user(username=username, password=password)
    client.force_login(user)


@pytest.mark.django_db
def test_feed_passing(client, set_default_language):
    uri = reverse('home')
    resp = client.get(uri)
    content = resp.content.decode(resp.charset)
    assert 'Notice! Ads are displayed only in the selected language.' in content
