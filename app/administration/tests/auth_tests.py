import pytest
from django.urls import reverse

from django.test import Client
from pytest_django.asserts import assertTemplateUsed

from administration.tests.user_factory import UserFactory


@pytest.mark.django_db
@pytest.fixture
def active_admin_user():
    return UserFactory.create(is_staff=True, is_active=True)


@pytest.mark.django_db
@pytest.fixture
def inactive_admin_user():
    return UserFactory.create(is_staff=True, is_active=False)


@pytest.fixture
def client():
    return Client()


@pytest.mark.django_db
def test_active_staff_user_can_access_admin_url(client, active_admin_user):
    """
    Test that user that active user with is_staff attribute can access the administration.
    """
    client.force_login(user=active_admin_user)
    admin_url = reverse("administration:room_list")
    response = client.get(admin_url)

    assert response.status_code == 200
    assertTemplateUsed(response=response, template_name="administration/room_list.html")


@pytest.mark.django_db
def test_inactive_staff_user_cannot_access_admin_url(client, inactive_admin_user):
    """
    Test that user that inactive user with is_staff attribute cannot access the administration.
    """
    client.force_login(user=inactive_admin_user)
    admin_url = reverse("administration:room_list")
    response = client.get(admin_url)
    assert response.status_code == 404


def test_anonymous_user_cannot_access_admin_url(client):
    """
    Test that anonymous user cannot access the administration.
    """
    admin_url = reverse("administration:room_list")
    response = client.get(admin_url)
    assert response.status_code == 404
