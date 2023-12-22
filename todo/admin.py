import subprocess
from django.contrib import admin
from .models import User, Task, TaskTag
from django.contrib import messages


@admin.action(description="Run Black Formatter on todo app")
def run_black(modeladmin, request, queryset):
    try:
        subprocess.run(
            ["black", "./todo"],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        modeladmin.message_user(
            request, "Black formatting completed successfully", messages.SUCCESS
        )
    except subprocess.CalledProcessError as e:
        modeladmin.message_user(request, e.stderr.decode(), messages.ERROR)


@admin.action(description="Run Flake8 Linting on todo app")
def run_flake8(modeladmin, request, queryset):
    try:
        process = subprocess.run(
            ["flake8", "./todo", "--extend-ignore=E501"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        if process.stdout:
            modeladmin.message_user(
                request, "Flake8 issues detected:\n" + process.stdout, messages.WARNING
            )
        elif process.stderr:
            modeladmin.message_user(
                request, "Flake8 error:\n" + process.stderr, messages.ERROR
            )
        else:
            modeladmin.message_user(
                request, "Flake8 linting passed with no issues", messages.SUCCESS
            )
    except Exception as e:
        modeladmin.message_user(request, str(e), messages.ERROR)


class UserAdmin(admin.ModelAdmin):
    actions = [run_black, run_flake8]


class TaskAdmin(admin.ModelAdmin):
    actions = [run_black, run_flake8]


class TaskTagAdmin(admin.ModelAdmin):
    actions = [run_black, run_flake8]


admin.site.register(User, UserAdmin)
admin.site.register(Task, TaskAdmin)
admin.site.register(TaskTag, TaskTagAdmin)
