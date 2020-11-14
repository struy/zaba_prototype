import pytest
from selenium import webdriver


@pytest.fixture
def supply_url():
    return "https://zaba.today/api"


@pytest.fixture(scope="module")
def driver():
    driver = webdriver.Chrome()
    yield driver
    driver.quit()
