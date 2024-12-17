from django.contrib import admin

from employees.models import Employee


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = (
        "username",
        "last_name",
        "first_name",
        "email",
        "is_active",
    )

    list_filter = (
        "is_superuser",
        "is_active",
        "is_staff",
    )

    ordering = (
        "-is_active",
        "last_name",
    )

    search_fields = (
        "username",
        "email",
        "first_name",
        "last_name",
    )
