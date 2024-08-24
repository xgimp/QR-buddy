import pytest
from django.test import Client
from django.urls import reverse
from pytest_django.asserts import assertTemplateUsed

from administration.tests.user_factory import UserFactory
from chat.tests.chat_room_factory import ChatRoomFactory


@pytest.fixture
def authenticated_client():
    active_admin_user = UserFactory.create(is_staff=True, is_active=True)
    client = Client()
    client.force_login(user=active_admin_user)
    return client


@pytest.mark.django_db
def test_right_template_used_for_room_list_page(authenticated_client):
    """
    Test that the right template - room_list.html is used for admin RoomListView.
    """
    index_url = reverse("administration:room_list")
    response = authenticated_client.get(index_url)
    assertTemplateUsed(response, template_name="administration/room_list.html")


@pytest.mark.django_db
def test_room_in_template_context(authenticated_client):
    """
    Test that existing room PK is in template context (Therefore should be displayed in admin).
    """
    room = ChatRoomFactory.create()
    index_url = reverse("administration:room_list")
    response = authenticated_client.get(index_url)
    assertTemplateUsed(response, template_name="administration/room_list.html")
    assert response.context["chatroom_list"].first().pk == room.pk


@pytest.mark.django_db
def test_right_template_used_for_add_room_page(authenticated_client):
    """
    Test that the right template - add_room_form.html is used for admin RoomCreateView.
    """
    add_room_url = reverse("administration:create_room")
    response = authenticated_client.get(add_room_url)
    assertTemplateUsed(response, template_name="administration/add_room_form.html")


@pytest.mark.django_db
def test_right_template_used_for_delete_room_page(authenticated_client):
    """
    Test that the right template - room_confirm_delete.html is used for admin RoomDeleteView.
    """
    room = ChatRoomFactory.create()
    delete_room_url = reverse(
        "administration:delete_room", kwargs={"room_pk": str(room.pk)}
    )
    response = authenticated_client.get(delete_room_url)
    assertTemplateUsed(
        response, template_name="administration/room_confirm_delete.html"
    )
