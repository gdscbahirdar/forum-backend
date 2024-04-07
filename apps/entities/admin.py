from django.contrib import admin

from apps.entities.models.admin_models import FacultyAdmin
from apps.entities.models.faculty_models import Department, Faculty
from apps.entities.models.student_models import Student
from apps.entities.models.teacher_models import Teacher


class DepartmentInline(admin.TabularInline):
    model = Department
    extra = 1


class FacultyAdminInline(admin.StackedInline):
    model = FacultyAdmin
    can_delete = False


class FacultyAdmin(admin.ModelAdmin):
    inlines = [
        DepartmentInline,
        FacultyAdminInline,
    ]
    list_display = ("name", "description")
    search_fields = ("name",)


admin.site.register(Faculty, FacultyAdmin)


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ("student_id", "first_name", "last_name", "department", "year_in_school")
    search_fields = ("student_id", "first_name", "last_name")
    list_filter = ("faculty", "department", "year_in_school")


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ("user", "first_name", "last_name", "faculty")
    search_fields = ("user__username", "first_name", "last_name")
    list_filter = ("faculty", "departments")
