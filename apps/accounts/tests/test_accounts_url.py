import pytest

pytestmark = pytest.mark.django_db


@pytest.mark.parametrize("url, status", [

    ('/en/accounts/login/', 200),
    ('/en/accounts/logout/', 200),
    ('/en/accounts/password_reset/', 200),
    ('/en/accounts/password_reset/done/', 200),
    ('/en/accounts/password_change/', 302),
    ('/en/accounts/password_change/done/', 302),
    ('/en/accounts/register/', 200),
    ('/en/accounts/edit/', 302),
    ('/en/accounts/favorites/', 302),
    ('/en/accounts/my_ads/', 302),
    # ('/en/accounts/connect_user/....')
    # ('reset/<uidb64>/<token>/',
    # password_reset/done/'

])
def test_static_urls(client, url, status):
    assert client.get(url).status_code == status


@pytest.mark.parametrize("url, status", [
    ('/en/accounts/edit/', 200),
    ('/en/accounts/favorites/', 200),
    ('/en/accounts/my_ads/', 200),
    ('/en/accounts/password_change/', 200),
    ('/en/accounts/password_change/done/', 200)

])
def test_static_auth_urls(admin_client, url, status):
    assert admin_client.get(url).status_code == status
