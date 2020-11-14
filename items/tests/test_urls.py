from django.urls import reverse, resolve


class TestUrls:

    def test_detail_url(self):
        path = reverse('items:detail', kwargs={'advert_id': 1})
        assert resolve(path).view_name == 'items:detail'
