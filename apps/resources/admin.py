from django.contrib import admin
from apps.resources.models.resource_models import Resource, ResourceCategory, ResourceFile


class ResourceFileInline(admin.TabularInline):
    model = ResourceFile
    extra = 1
    readonly_fields = ["file_type", "file_size"]


@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = ("title", "user", "created_at", "updated_at")
    search_fields = ("title", "description", "user__username")
    list_filter = ("categories", "tags", "created_at", "updated_at")
    inlines = [ResourceFileInline]


@admin.register(ResourceCategory)
class ResourceCategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(ResourceFile)
class ResourceFileAdmin(admin.ModelAdmin):
    list_display = ("resource", "file", "file_type", "file_size")
    search_fields = ("resource__title",)
