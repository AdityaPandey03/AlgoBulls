from django.contrib import admin
from django.urls import path
from todo.views import UserViewSet, TaskViewSet

urlpatterns = [
    # user api's
    path("admin/", admin.site.urls),
    path("api/signup/", UserViewSet.as_view({"post": "user_signup"})),
    path("api/login/", UserViewSet.as_view({"post": "user_login"})),
    # task api's
    path("api/create-task/", TaskViewSet.as_view({"post": "create_task"})),
    path(
        "api/task/<int:id>/", TaskViewSet.as_view({"get": "get_task"}), name="get_task"
    ),
    path(
        "api/all-tasks/",
        TaskViewSet.as_view({"get": "get_all_tasks"}),
        name="all_tasks",
    ),
    path("api/delete-task/", TaskViewSet.as_view({"post": "delete_task"})),
    path("api/update-task/", TaskViewSet.as_view({"post": "update_task"})),
]
