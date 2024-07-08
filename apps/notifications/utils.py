from django.contrib.contenttypes.models import ContentType

from apps.forum.models.qa_models import Post
from apps.notifications.models.notification_models import Notification
from apps.notifications.models.notification_models import Subscription


def notify_user(
    user: object, title: str, message: str | None = None, level: str = "info", target: object = None
) -> object:
    """
    Notifies a user with a given title and message.

    Args:
        user (object): The user to notify.
        title (str): The title of the notification.
        message (str, optional): If not provided, the title will be used as the message.
        level (str, optional): The level of the notification. Defaults to "info".
        target (object, optional): The target object associated with the notification.

    Returns:
        object: The created notification object.
    """
    if not message:
        message = title

    if level not in Notification.Level.values:
        level = Notification.Level.INFO

    notification_kwargs = {
        "user": user,
        "title": title,
        "message": message,
        "level": level,
    }

    if target:
        notification_kwargs["target_content_type"] = ContentType.objects.get_for_model(target)
        notification_kwargs["target_object_id"] = target.pk

    notification = Notification.objects.create(**notification_kwargs)
    return notification


def notify_subscribers(title, message, level, target):
    """
    Notifies the subscribers about a new notification.

    Args:
        title (str): The title of the notification.
        message (str): The message content of the notification.
        level (str): The level of the notification (e.g., 'info', 'warning', 'error').
        target (object): The target object for which the notification is being sent.

    Returns:
        list: A list of newly created notifications.

    """
    target_content_type = ContentType.objects.get_for_model(target)
    subscriptions = Subscription.objects.filter(target_content_type=target_content_type, target_object_id=target.pk)

    new_notifications = []

    for subscription in subscriptions:
        notification = notify_user(
            user=subscription.user,
            title=title,
            message=message,
            level=level,
            target=target,
        )
        new_notifications.append(notification)

    return new_notifications


def create_subscription(user: object, target: object):
    """
    Create a subscription for a user to a target object.

    Args:
        user (object): The user object for whom the subscription is created.
        target (object): The target object to which the user is subscribing.

    Returns:
        Subscription: The created subscription object.

    """
    target_content_type = ContentType.objects.get_for_model(target)
    return Subscription.objects.create(user=user, target_content_type=target_content_type, target_object_id=target.pk)


def notify_if_not_owner(instance, title, message):
    """
    Notifies the subscribers if the user is not the owner of the target object.

    Args:
        instance: The instance object.
        title: The title of the notification.
        message: The message of the notification.
    """
    target = instance.content_object
    if target.user != instance.user:
        if isinstance(target, Post):
            target = getattr(target, "question", getattr(target, "answer", target))

        notify_subscribers(
            title=title,
            message=message,
            level=Notification.Level.INFO,
            target=target,
        )
