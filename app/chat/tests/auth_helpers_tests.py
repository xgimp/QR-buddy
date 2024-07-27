import pytest

from chat.auth import is_valid_uuid, is_permitted


@pytest.mark.parametrize(
    "valid_uuid",
    [
        "f15a56bc-71cf-46ff-85a9-a2b0b10e1fa3",
        "90640e71-c348-4a1f-8653-f70915744e48",
        "b9f06acc-0873-4de5-850d-4134830fa246",
        "9c1709b2-0789-4638-a168-840e44890e83",
        "fad68121-fee5-4bd3-b520-726a08cefb0b",
        "e1605290-6fbe-4545-9bde-7b70a9a07af4",
        "dc4652a1-1ba8-46e2-9c4a-28e1a6019e57",
        "5043d99c-25f7-4433-b9e3-f1f966c80ec0",
        "9b6bf237-43db-4b30-8f44-c75ab8c6badd",
        "325f7f9a-5dd5-427b-86cc-0586bea12f20",
        "00000000-0000-0000-0000-000000000000",
    ],
)
def test_is_valid_uuid_v4_true(valid_uuid):
    """
    Test that is_valid_uuid() returns True if valid UUID v4 is given.
    """
    assert is_valid_uuid(valid_uuid) is True


@pytest.mark.parametrize("invalid_uuid", ["", "test", 1, "\n", {}, []])
def test_is_valid_uuid_v4_false(invalid_uuid):
    """
    Test that is_valid_uuid() returns False if invalid UUID v4 is given.
    """
    assert is_valid_uuid(invalid_uuid) is False


def test_is_permitted_false_if_invalid_room_name():
    """
    Test that is_permitted() returns False if invalid 'room_name' UUID is given.
    """
    invalid_room_name_uuid = "invalid uuid v4"
    valid_user_id = "37150f03-c045-483b-b842-2000c6c4ccf4"
    assert is_permitted(invalid_room_name_uuid, valid_user_id) is False


def test_is_permitted_false_if_invalid_user_id():
    """
    Test that is_permitted() returns False if invalid 'invalid_user_id' UUID is given.
    """
    valid_room_name_uuid = "37150f03-c045-483b-b842-2000c6c4ccf4"
    invalid_user_id = "invalid user_id"
    assert is_permitted(valid_room_name_uuid, invalid_user_id) is False
