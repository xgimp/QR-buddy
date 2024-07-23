from chat.auth import is_valid_uuid, is_permitted


def test_is_valid_uuid_v4_true():
    """
    Test that is_valid_uuid() returns True if valid UUID v4 is given.
    """
    valid_uuid_v4_str = "37150f03-c045-483b-b842-2000c6c4ccf4"
    assert is_valid_uuid(valid_uuid_v4_str, version=4) is True


def test_is_valid_uuid_v4_false():
    """
    Test that is_valid_uuid() returns False if invalid UUID v4 is given.
    """
    invalid_uuid_v4_str = "invalid uuid v4"
    assert is_valid_uuid(invalid_uuid_v4_str, version=4) is False


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
