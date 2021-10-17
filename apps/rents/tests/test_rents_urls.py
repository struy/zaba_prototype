import pytest
from django.contrib.auth.models import User
from model_bakery import baker
from model_bakery.random_gen import gen_email

pytestmark = pytest.mark.django_db


@pytest.fixture()
def rents():
    user = baker.make(User, email=gen_email)
    return baker.make('rents.Rental', local='en', author=user, _quantity=10)


@pytest.mark.parametrize("url, status", [
    ('/en/rents/', 200),
    ('/en/rents/1/', 200),
    ('/en/rents/map/', 200),
    ('/en/rents/table/', 200),
    ('/en/rents/edit/1', 302),
    ('/en/rents/delete/1', 302),
    ('/en/rents/100000', 301)
])
def test_item_urls(client, rents, url, status):
    assert client.get(url).status_code == status


@pytest.mark.parametrize("url", [
    '/en/rents/edit/1',
    '/en/rents/delete/1'
])
def test_item_auth_urls(admin_client, url, rents):
    assert admin_client.get(url).status_code == 200
