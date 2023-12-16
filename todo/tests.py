from todo.models import User, Task, TaskTag
from rest_framework.test import APITestCase, APIClient


class CustomAuthenticationTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(username="testuser", password="testpassword")

    def test_authentication_failure_invalid_token(self):
        self.client.credentials(HTTP_AUTHORIZATION="InvalidToken")
        response = self.client.get("/api/all-tasks/")
        self.assertEqual(response.status_code, 403)
        self.assertIn("detail", response.data)
        self.assertEqual(response.data["detail"], "No such user")


class UserAPITestCase(APITestCase):
    def test_user_signup_success(self):
        response = self.client.post(
            "/api/signup/", {"username": "newuser", "password": "dummy"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("login_token", response.data)

    def test_user_signup_failure_user_exists(self):
        User.objects.create(username="existinguser", password="password")
        response = self.client.post(
            "/api/signup/", {"username": "existinguser", "password": "dummy"}
        )
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.data["message"], "User already exists")

    def test_signup_without_password(self):
        response = self.client.post("/api/signup/", {"username": "newuser"})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["message"], "Password is required")

    def test_user_login_success(self):
        self.client.post(
            "/api/signup/", {"username": "testuser", "password": "testpassword"}
        )
        response = self.client.post(
            "/api/login/", {"username": "testuser", "password": "testpassword"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("message", response.data)

    def test_user_login_failure_incorrect_username(self):
        response = self.client.post(
            "/api/login/", {"username": "wronguser", "password": "testpass"}
        )
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data["message"], "Please check the username")

    def test_user_login_failure_incorrect_password(self):
        User.objects.create(username="testuser", password="testpassword")
        response = self.client.post(
            "/api/login/", {"username": "testuser", "password": "wrongpass"}
        )
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data["message"], "Incorrect Password")

    def test_custom_authentication_success(self):
        signup_response = self.client.post(
            "/api/signup/", {"username": "adi", "password": "dummy"}
        )
        self.assertEqual(signup_response.status_code, 200)
        token = signup_response.json().get("login_token")

        self.client.credentials(HTTP_AUTHORIZATION=token)

        user = User.objects.get(username="adi")
        Task.objects.create(
            user=user,
            title="Sample Task",
            description="Description",
            due_date="2023-12-25",
            status="OPEN",
        )

        response = self.client.get("/api/all-tasks/")

        self.assertEqual(response.status_code, 200)


class TaskAPITestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(username="testuser", password="testpassword")
        self.client.force_authenticate(user=self.user)
        self.user_without_tasks = User.objects.create(
            username="user_without_tasks", password="password"
        )
        self.task = Task.objects.create(
            user=self.user,
            title="Sample Task",
            description="Description",
            status="OPEN",
        )
        TaskTag.objects.create(task=self.task, user=self.user, tag="tag1")

    def test_create_task_success(self):
        response = self.client.post(
            "/api/create-task/",
            {
                "title": "first post",
                "description": "hey",
                "due_date": "2023-12-25",
                "status": "OPEN",
                "tags": ["post", "blog"],
            },
        )
        self.assertEqual(response.status_code, 200)
        task_id = response.json().get("task_id")
        self.assertTrue(Task.objects.filter(id=task_id).exists())

    def test_create_task_invalid_status(self):
        response = self.client.post(
            "/api/create-task/",
            {
                "title": "second post",
                "description": "hey again",
                "due_date": "2023-12-30",
                "status": "NOT_OPEN",
                "tags": ["work", "update"],
            },
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["message"], "Invalid status")

    def test_get_task_success(self):
        task_id = self.task.id
        response = self.client.get(f"/api/task/{task_id}/")
        self.assertEqual(response.status_code, 200)

    def test_create_task_without_title(self):
        task_data = {
            "description": "A test task description",
            "due_date": "2023-12-30",
            "status": "NOT_OPEN",
            "tags": ["work", "update"],
        }

        response = self.client.post("/api/create-task/", task_data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["message"], "Title is required")

    def test_create_task_without_description(self):
        task_data = {
            "title": "second post",
            "due_date": "2023-12-30",
            "status": "NOT_OPEN",
            "tags": ["work", "update"],
        }

        response = self.client.post("/api/create-task/", task_data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["message"], "Description is required")

    def test_create_task_with_default_status(self):
        response = self.client.post(
            "/api/create-task/",
            {
                "title": "Test Task",
                "description": "Test Description",
                "tags": ["tag1", "tag2"],
            },
        )
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        task_id = response_data.get("task_id")
        created_task = Task.objects.get(id=task_id)
        self.assertEqual(created_task.status, "OPEN")

    def test_get_task_not_found(self):
        non_existent_task_id = 99999
        response = self.client.get(f"/api/task/{non_existent_task_id}/")
        self.assertEqual(response.status_code, 404)

    def test_get_task_invalid_id_format(self):
        response = self.client.get("/api/task/?id=invalid")
        self.assertEqual(response.status_code, 404)

    def test_get_task_unauthorized_user(self):
        another_user = User.objects.create(username="otheruser", password="password")
        self.client.force_authenticate(user=another_user)
        response = self.client.get(f"/api/task/?id={self.task.id}")
        self.assertEqual(response.status_code, 404)

    def test_get_all_tasks_success(self):
        response = self.client.get("/api/all-tasks/")
        self.assertEqual(response.status_code, 200)
        tasks_data = response.json()["message"]
        self.assertTrue(any(task["id"] == self.task.id for task in tasks_data))

    def test_get_all_tasks_no_tasks_user(self):
        self.client.force_authenticate(user=self.user_without_tasks)
        response = self.client.get("/api/all-tasks/")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data["message"], "No such user")

    def test_update_task_success(self):
        response = self.client.post(
            f"/api/update-task/?id={self.task.id}",
            {
                "title": "Updated Title",
                "description": "Updated Description",
                "due_date": "2023-12-25",
                "status": "OPEN",
                "tags": ["Updated", "Tags"],
            },
        )
        self.assertEqual(response.status_code, 200)
        updated_task = Task.objects.get(id=self.task.id)
        self.assertEqual(updated_task.title, "Updated Title")

    def test_update_nonexistent_task(self):
        nonexistent_task_id = self.task.id + 1
        response = self.client.post(
            f"/api/update-task/?id={nonexistent_task_id}",
            {"title": "New Title", "status": "OPEN"},
        )
        self.assertEqual(response.status_code, 404)

    def test_update_task_invalid_status(self):
        response = self.client.post(
            f"/api/update-task/?id={self.task.id}",
            {"title": "New Title", "status": "INVALID_STATUS"},
        )
        self.assertEqual(response.status_code, 400)

    def test_update_task_unauthorized_user(self):
        new_user = User.objects.create(username="otheruser", password="password")
        self.client.force_authenticate(user=new_user)
        response = self.client.post(
            f"/api/update-task/?id={self.task.id}",
            {"title": "New Title", "status": "OPEN"},
        )
        self.assertEqual(response.status_code, 401)

    def test_delete_task_success(self):
        response = self.client.post(f"/api/delete-task/?id={self.task.id}")
        self.assertEqual(response.status_code, 204)
        self.assertFalse(Task.objects.filter(id=self.task.id).exists())

    def test_delete_nonexistent_task(self):
        nonexistent_task_id = self.task.id + 1
        response = self.client.post(f"/api/delete-task/?id={nonexistent_task_id}")
        self.assertEqual(response.status_code, 404)

    def test_delete_task_unauthorized_user(self):
        another_user = User.objects.create(username="otheruser", password="password")
        self.client.force_authenticate(user=another_user)
        response = self.client.post(f"/api/delete-task/?id={self.task.id}")
        self.assertEqual(response.status_code, 401)
