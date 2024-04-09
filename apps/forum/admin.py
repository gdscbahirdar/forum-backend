from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline

from apps.forum.models.comment_models import Comment
from apps.forum.models.qa_models import Answer, Post, Question
from apps.forum.models.tag_models import Tag


class CommentInline(GenericTabularInline):
    model = Comment
    extra = 1


class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 1


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ["user", "body", "vote_count", "created_at"]
    search_fields = ["body"]
    list_filter = ["created_at"]
    date_hierarchy = "created_at"


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ["title", "is_answered", "is_closed", "view_count", "answer_count", "get_created_at"]
    search_fields = ["title", "post__body"]
    list_filter = ["is_answered", "is_closed", "post__created_at"]
    prepopulated_fields = {"slug": ("title",)}

    def get_created_at(self, obj):
        return obj.post.created_at

    get_created_at.admin_order_field = "post__created_at"
    get_created_at.short_description = "Created At"

    inlines = [CommentInline, AnswerInline]


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ["__str__", "get_created_at"]
    search_fields = ["post__body"]
    list_filter = ["post__created_at"]

    def get_created_at(self, obj):
        return obj.post.created_at

    get_created_at.admin_order_field = "post__created_at"
    get_created_at.short_description = "Created At"

    inlines = [CommentInline]


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ["name", "created_at"]
    search_fields = ["name"]
    list_filter = ["created_at"]
