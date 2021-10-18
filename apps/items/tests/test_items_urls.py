import pytest
from django.contrib.auth.models import User
from model_bakery import baker
from model_bakery.random_gen import gen_email

pytestmark = pytest.mark.django_db


@pytest.fixture()
def items():
    user = baker.make(User, email=gen_email)
    return baker.make('items.Item', local='en', author=user, _quantity=10)


@pytest.mark.parametrize("url, status", [
    ('/en/items/', 200),
    ('/en/items/1/', 200),
    ('/en/items/map/', 200),
    ('/en/items/table/', 200),
    ('/en/items/edit/1/', 302),
    ('/en/items/delete/1/', 302),
    ('/en/items/100000/', 404)
])
def test_item_urls(client, items, url, status):
    assert client.get(url).status_code == status


@pytest.mark.parametrize("url", [
    '/en/items/edit/1/',
    '/en/items/delete/1/',
    '/en/items/new/'
])
def test_item_auth_urls(admin_client, url, items):
    assert admin_client.get(url).status_code == 200
