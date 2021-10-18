import pytest

pytestmark = pytest.mark.django_db


@pytest.mark.parametrize("url, status", [
    ('/en/contact/', 200),
    ('/en/success/', 200),
    ('/en/no_success/', 200)
])
def test_item_urls(client, url, status):
    assert client.get(url).status_code == status
