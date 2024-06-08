from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.content_actions.models.bookmark_models import Bookmark
from apps.content_actions.models.comment_models import Comment
from apps.content_actions.models.vote_models import Vote
from apps.forum.models.qa_models import Answer, Question
from apps.notifications.models.notification_models import Notification
from apps.notifications.utils import create_subscription, notify_if_not_owner, notify_subscribers
from apps.resources.models.resource_models import Resource


@receiver(post_save, sender=Question)
@receiver(post_save, sender=Answer)
@receiver(post_save, sender=Resource)
def subscribe_owner(sender, instance, created, **kwargs):
    """
    Signal receiver function that subscribes the owner of a newly created instance to receive notifications.
    """
    if created:
        user = None
        if hasattr(instance, "user"):
            user = instance.user
        elif hasattr(instance, "post") and hasattr(instance.post, "user"):
            user = instance.post.user

        if user is not None:
            create_subscription(user, instance)


@receiver(post_save, sender=Answer)
def create_answer_notification(sender, instance, created, **kwargs):
    """
    Creates a notification when a new answer is created for a question.
    """
    if created and instance.question.post.user != instance.post.user:
        notify_subscribers(
            title="New Answer",
            message="Question received a new answer",
            level=Notification.Level.INFO,
            target=instance.question,
        )


@receiver(post_save, sender=Comment)
def create_comment_notification(sender, instance, created, **kwargs):
    """
    Creates a notification for a new comment.
    """
    if created:
        notify_if_not_owner(
            instance, "New Comment", f"{type(instance.content_object).__name__} received a new comment"
        )


@receiver(post_save, sender=Vote)
def create_vote_notification(sender, instance, created, **kwargs):
    """
    Creates a notification when a new vote is created.
    """
    if created:
        notify_if_not_owner(
            instance, "New Vote", f"{type(instance.content_object).__name__} received an {instance.vote_type}"
        )


@receiver(post_save, sender=Bookmark)
def create_bookmark_notification(sender, instance, created, **kwargs):
    """
    Creates a notification when a new bookmark is created.
    """
    if created:
        notify_if_not_owner(instance, "New Bookmark", f"{type(instance.content_object).__name__} got bookmarked")
