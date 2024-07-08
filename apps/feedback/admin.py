from django.contrib import admin

from apps.feedback.models.feedback_models import Feedback, FeedbackReply


class FeedbackReplyInline(admin.TabularInline):
    model = FeedbackReply
    extra = 1


class FeedbackAdmin(admin.ModelAdmin):
    inlines = [FeedbackReplyInline]


admin.site.register(Feedback, FeedbackAdmin)
