import pytest
from django.test import Client
from django.urls import reverse
from pytest_django.asserts import assertTemplateUsed


@pytest.fixture
def client():
    return Client()


def test_index_template_is_used_on_homepage(client):
    """
    Test that the right template - index.html is used for app's index page.
    """
    index_url = reverse("qr_pair:index_view")
    response = client.get(index_url)
    assertTemplateUsed(response, template_name="index.html")
