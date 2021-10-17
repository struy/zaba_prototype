import pytest
from django.contrib.auth.models import User
from model_bakery import baker
from model_bakery.random_gen import gen_email

pytestmark = pytest.mark.django_db


@pytest.fixture()
def gifts():
    user = baker.make(User, email=gen_email)
    return baker.make('gifts.Gift', local='en', author=user, _quantity=10)


@pytest.mark.parametrize("url, status", [
    ('/en/gifts/', 200),
    ('/en/gifts/1/', 200),
    ('/en/gifts/map/', 200),
    ('/en/gifts/table/', 200),
    ('/en/gifts/edit/1', 302),
    ('/en/gifts/delete/1', 302),
    ('/en/gifts/100000', 301)
])
def test_item_urls(client, gifts, url, status):
    assert client.get(url).status_code == status


@pytest.mark.parametrize("url", [
    '/en/gifts/edit/1',
    '/en/gifts/delete/1'
])
def test_item_auth_urls(admin_client, url, gifts):
    assert admin_client.get(url).status_code == 200
