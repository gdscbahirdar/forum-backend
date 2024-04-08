import uuid


def generate_password(first_name, middle_name, last_name):
    return "123idiot"  # TODO Find a logic to generate password from the name


def is_valid_uuid(value, version=4):
    """
    Check if value is a valid UUID.

    Parameters:
        value (str): The UUID string to test.
        version (int): The version of the UUID to check against. Default is 4.

    Returns:
        bool: True if value is a valid UUID, False otherwise.
    """
    try:
        uuid.UUID(value, version=version)
        return True
    except ValueError:
        return False
