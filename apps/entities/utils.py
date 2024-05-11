import uuid


def generate_password(last_name: str) -> str:
    """
    Generates a password based on the last name for first-time users.

    Args:
        last_name (str): The last name to generate the password from.

    Returns:
        str: The generated password.

    """
    return last_name.lower() + "1234#"


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
