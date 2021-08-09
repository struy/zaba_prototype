import pytest
from django.urls import reverse


def test_an_admin_view(admin_client):
    response = admin_client.get('/admin/')
    assert response.status_code == 200


def test_with_authenticated_client(client, django_user_model):
    username = "user1"
    password = "bar"
    user = django_user_model.objects.create_user(username=username, password=password)
    client.force_login(user)


@pytest.mark.django_db
def test_feed_passing(client):
    uri = reverse('home')
    resp = client.get(uri)
    content = resp.content.decode(resp.charset)
    assert 'Notice! Ads are displayed only in the selected language.' in content

# soup = bs4.BeautifulSoup(content, 'html.parser')
# assert soup.select_one('h1#title-headliner') == '<h1>title</h1>'


# @pytest.mark.parametrize("userid, firstname", [(1, "George"), (2, "Janet")])
# def test_list_valid_user(supply_url, userid, firstname):
#     url = supply_url + "/users/" + str(userid)
#     resp = requests.get(url)
#     j = json.loads(resp.text)
#     assert resp.status_code == 200, resp.text
#     assert j['data']['id'] == userid, resp.text
#     assert j['data']['first_name'] == firstname, resp.text
#
#
# def test_list_invaliduser(supply_url):
#     url = supply_url + "/users/50"
#     resp = requests.get(url)
#     assert resp.status_code == 404, resp.text
