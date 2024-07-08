import factory
from django.contrib.contenttypes.models import ContentType

from apps.forum.models.qa_models import Question
from apps.forum.tests.factories import QuestionFactory
from apps.notifications.models.notification_models import Subscription


class SubscriptionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Subscription

    target_content_type = factory.LazyAttribute(lambda obj: ContentType.objects.get_for_model(Question))
    target_object_id = factory.SelfAttribute("target.id")
    target = factory.SubFactory(QuestionFactory)
