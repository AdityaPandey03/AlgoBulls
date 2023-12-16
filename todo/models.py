from django.db import models


class User(models.Model):
    MAX_USERNAME_LENGTH = 200
    MAX_PASSWORD_LENGTH = 30
    LOGIN_TOKEN_MAX_LENGTH = 100

    username = models.CharField(max_length=MAX_USERNAME_LENGTH, unique=True)
    password = models.CharField(max_length=MAX_PASSWORD_LENGTH)
    login_token = models.CharField(
        max_length=LOGIN_TOKEN_MAX_LENGTH, unique=True, null=True
    )


class Task(models.Model):
    MAX_TITLE_LENGTH = 100
    MAX_DESCRIPTION_LENGTH = 1000
    MAX_STATUS_LENGTH = 7
    STATUS_CHOICES = [
        (
            "OPEN",
            "Open",
        ),  # here, first element is the value that will be stored in the DataBase
        (
            "WORKING",
            "Working",
        ),  # second element is the value that is for frontEnd(human readable)
        ("DONE", "Done"),
        ("OVERDUE", "Overdue"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, editable=False)
    timestamp = models.DateTimeField(auto_now_add=True, editable=False)
    title = models.CharField(max_length=MAX_TITLE_LENGTH, blank=False)
    description = models.CharField(
        max_length=MAX_DESCRIPTION_LENGTH, blank=False
    )
    due_date = models.DateField(null=True, blank=True)
    status = models.CharField(
        max_length=MAX_STATUS_LENGTH,
        choices=STATUS_CHOICES,
        default="Open",
        blank=False,
    )


class TaskTag(models.Model):
    MAX_TAG_LENGTH = 50

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="task_tags")
    tag = models.CharField(max_length=MAX_TAG_LENGTH, null=True, blank=True)
