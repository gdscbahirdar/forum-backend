from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline

from apps.forum.models.qa_meta_models import Bookmark, Comment, Tag, Vote
from apps.forum.models.qa_models import Answer, Post, Question


class CommentInline(GenericTabularInline):
    model = Comment
    extra = 1


class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 1


class VoteInline(GenericTabularInline):
    model = Vote
    extra = 0


class BookmarkInline(GenericTabularInline):
    model = Bookmark
    extra = 0


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ["user", "body", "vote_count", "created_at"]
    search_fields = ["body"]
    list_filter = ["created_at"]
    date_hierarchy = "created_at"
    inlines = [CommentInline, VoteInline, BookmarkInline]


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

    inlines = [AnswerInline, VoteInline, BookmarkInline]


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ["__str__", "get_created_at"]
    search_fields = ["post__body"]
    list_filter = ["post__created_at"]

    def get_created_at(self, obj):
        return obj.post.created_at

    get_created_at.admin_order_field = "post__created_at"
    get_created_at.short_description = "Created At"

    inlines = [VoteInline, BookmarkInline]


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ["name", "created_at"]
    search_fields = ["name"]
    list_filter = ["created_at"]


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ["user", "content_object", "text", "created_at"]
    search_fields = ["text"]
    list_filter = ["created_at"]
    inlines = [VoteInline]


@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ["user", "vote_type", "content_type", "object_id", "content_object"]
    search_fields = ["user__username", "vote_type"]
    list_filter = ["vote_type", "content_type"]


@admin.register(Bookmark)
class BookmarkAdmin(admin.ModelAdmin):
    list_display = ["user", "content_type", "object_id", "content_object"]
    search_fields = [
        "user__username",
    ]
    list_filter = ["content_type"]
