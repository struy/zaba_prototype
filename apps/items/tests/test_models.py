import pytest


@pytest.mark.django_db
class TestModels:
    pass

    # def test_item_is_condition_default(self):
    #     item = mixer.blend('items.Item', title="Test pytest")
    #     assert item.condition == '0'
    #
    # def test_item_is_condition_set(self):
    #     item = mixer.blend('items.Item', condition=1)
    #     assert item.condition == '1'
