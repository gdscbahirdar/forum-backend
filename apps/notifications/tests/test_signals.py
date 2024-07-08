import pytest
from django.db.models.signals import post_save

from apps.forum.models.qa_models import Answer, Question
from apps.forum.tests.factories import AnswerFactory, QuestionFactory
from apps.notifications.models.notification_models import Notification

pytestmark = pytest.mark.unit


class TestNotificationSignals:
    def test_subscribe_owner(self, mock_create_subscription):
        instance = QuestionFactory.build()
        post_save.send(Question, instance=instance, created=True)
        mock_create_subscription.assert_called_with(instance.post.user, instance)

    def test_create_answer_notification(self, mock_create_subscription, mock_notify_subscribers):
        instance = AnswerFactory.build()
        post_save.send(Answer, instance=instance, created=True)
        mock_create_subscription.assert_called_with(instance.post.user, instance)
        mock_notify_subscribers.assert_called_with(
            title="New Answer",
            message="Question received a new answer",
            level=Notification.Level.INFO,
            target=instance.question,
        )
