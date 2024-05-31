from apps.content_actions.models.comment_models import Comment
from apps.forum.models.qa_models import Post
from apps.resources.models.resource_models import Resource

MODEL_MAPPING = {"post": Post, "comment": Comment, "resource": Resource}
