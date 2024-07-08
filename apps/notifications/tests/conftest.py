import pytest


@pytest.fixture
def mock_create_subscription(mocker):
    return mocker.patch("apps.notifications.signals.create_subscription")


@pytest.fixture
def mock_notify_subscribers(mocker):
    return mocker.patch("apps.notifications.signals.notify_subscribers")


@pytest.fixture
def mock_notify_if_not_owner(mocker):
    return mocker.patch("apps.notifications.signals.notify_if_not_owner")
