from django.contrib import admin
from apps.resources.models.resource_models import Resource, ResourceCategory, ResourceFile


class ResourceFileInline(admin.TabularInline):
    model = ResourceFile
    extra = 1


@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = ("title", "uploader", "created_at", "updated_at")
    search_fields = ("title", "description")
    list_filter = ("created_at", "updated_at")
    inlines = [ResourceFileInline]


@admin.register(ResourceCategory)
class ResourceCategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(ResourceFile)
class ResourceFileAdmin(admin.ModelAdmin):
    list_display = ("resource", "file")
    search_fields = ("resource__title",)
