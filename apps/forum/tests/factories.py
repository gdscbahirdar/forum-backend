import factory
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType

from apps.content_actions.models.bookmark_models import Bookmark
from apps.content_actions.models.vote_models import Vote
from apps.factories import UserFactory
from apps.forum.models.qa_meta_models import Tag
from apps.forum.models.qa_models import Answer, Post, Question

User = get_user_model()


class PostFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Post

    user = factory.SubFactory(UserFactory)
    body = factory.Faker("text")


class QuestionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Question

    post = factory.SubFactory(PostFactory)
    title = factory.Faker("sentence")
    slug = factory.Faker("slug")


class AnswerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Answer

    post = factory.SubFactory(PostFactory)
    question = factory.SubFactory(QuestionFactory)


class VoteFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Vote

    user = factory.SubFactory(UserFactory)
    vote_type = Vote.UPVOTE
    content_type = factory.LazyAttribute(lambda obj: ContentType.objects.get_for_model(Post))
    object_id = factory.SelfAttribute("content_object.id")
    content_object = factory.SubFactory(PostFactory)


class BookmarkFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Bookmark

    user = factory.SubFactory(UserFactory)
    content_type = factory.LazyAttribute(lambda obj: ContentType.objects.get_for_model(Post))
    object_id = factory.SelfAttribute("content_object.id")
    content_object = factory.SubFactory(PostFactory)


class TagFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Tag

    name = factory.Faker("word")
