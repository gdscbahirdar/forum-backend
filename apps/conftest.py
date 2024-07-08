import pytest
from rest_framework.test import APIClient

from apps.factories import UserFactory


@pytest.fixture
def api_client() -> APIClient:
    """
    Fixture to provide an API client.

    Returns:
        APIClient: An instance of the APIClient class.
    """
    return APIClient()


@pytest.fixture
def user():
    """
    Fixture to create a user.

    Returns:
        User: An instance of the User model.
    """
    return UserFactory.create()
