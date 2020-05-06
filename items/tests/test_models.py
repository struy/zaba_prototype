from mixer.backend.django import mixer
import pytest


@pytest.mark.django_db
class TestModels:

    def test_item_is_condition_default(self):
        item = mixer.blend('items.Item', title="Test pytest")
        assert item.condition == 0

