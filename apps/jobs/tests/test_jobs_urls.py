import pytest
from django.contrib.auth.models import User
from model_bakery import baker
from model_bakery.random_gen import gen_email

pytestmark = pytest.mark.django_db


@pytest.fixture()
def jobs():
    user = baker.make(User, email=gen_email)
    return baker.make('jobs.Job', local='en', author=user, _quantity=10)


@pytest.mark.parametrize("url, status", [
    ('/en/jobs/', 200),
    ('/en/jobs/1/', 200),
    ('/en/jobs/map/', 200),
    ('/en/jobs/table/', 200),
    ('/en/jobs/edit/1/', 302),
    ('/en/jobs/delete/1/', 302),
    ('/en/jobs/100000/', 404)
])
def test_item_urls(client, jobs, url, status):
    assert client.get(url).status_code == status


@pytest.mark.parametrize("url", [
    '/en/jobs/edit/1/',
    '/en/jobs/delete/1/'
])
def test_item_auth_urls(admin_client, url, jobs):
    assert admin_client.get(url).status_code == 200
