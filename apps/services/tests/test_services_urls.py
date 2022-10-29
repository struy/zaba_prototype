import pytest
from django.contrib.auth.models import User
from model_bakery import baker
from model_bakery.random_gen import gen_email

from apps.services.models import ServiceType

pytestmark = pytest.mark.django_db


@pytest.fixture()
def services():
    user = baker.make(User, email=gen_email)
    service_type = baker.make(ServiceType, name='Beauty', icon='beauty' )
    return baker.make('services.Service', local='en', service_type=service_type, author=user, _quantity=10)


@pytest.mark.parametrize("url, status", [
    ('/en/services/', 200),
    ('/en/services/1/', 200),
    ('/en/services/map/', 200),
    ('/en/services/table/', 200),
    ('/en/services/edit/1/', 302),
    ('/en/services/delete/1/', 302),
    ('/en/services/100000/', 404)
])
def test_item_urls(client, services, url, status):
    assert client.get(url).status_code == status


@pytest.mark.parametrize("url", [
    '/en/services/edit/1/',
    '/en/services/delete/1/',
    '/en/services/new/'
])
def test_item_auth_urls(admin_client, url, services):
    assert admin_client.get(url).status_code == 200
