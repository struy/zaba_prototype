import pytest

pytestmark = pytest.mark.django_db


@pytest.mark.parametrize("url, status", [
    ('/admin/', 302),
    ('/robots.txt', 200),
    ('/en/contact/', 200),
    ('/en/map/', 200),
    ('/en/items/map/', 200),
    ('/en/term-of-services/', 200),
    ('/en/privacy-policy/', 200),
    ('/en/term-of-services/', 200),
    ('/en/place-ad/', 200),
    ('/rosetta/', 302),
    ('/en/admin/', 404),
    ('/en/rosetta/', 404),

    # /social-auth/login/google-oauth2/

])
def test_static_urls(client, url, status):
    assert client.get(url).status_code == status


@pytest.mark.parametrize("url, status", [
    ('/admin/', 200),
    ('/rosetta/files/project/', 200),

])
def test_static_auth_urls(admin_client, url, status):
    assert admin_client.get(url).status_code == status
