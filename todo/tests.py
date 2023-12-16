from django.test import TestCase
from todo.models import Task, TaskTag, User
from rest_framework.test import APITestCase, APIClient


class UserAPITestCase(TestCase):
    def test_user_signup_success(self):
        response = self.client.post(
            "/api/signup/", {"username": "testuser", "password": "testpass"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("login_token", response.data)

    def test_user_signup_failure_user_exists(self):
        response = self.client.post(
            "/api/signup/", {"username": "testuser", "password": "testpass"}
        )
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.data["message"], "User already exists")


#     def test_user_login_success(self):
#         response = self.client.post("/api/login/", {"username": "testuser", "password": "testpass"})
#         self.assertEqual(response.status_code, 200)
#         self.assertIn("message", response.data)

#     def test_user_login_failure_incorrect_username(self):
#         response = self.client.post("/api/login/", {"username": "wronguser", "password": "testpass"})
#         self.assertEqual(response.status_code, 404)
#         self.assertEqual(response.data["message"], "Please check the username")

#     def test_user_login_failure_incorrect_password(self):
#         response = self.client.post("/api/login/", {"username": "testuser", "password": "wrongpass"})
#         self.assertEqual(response.status_code, 401)
#         # import pdb
#         # pdb.set_trace()
#         self.assertEqual(response.data["message"], "Incorrect Password")

#     # def test_signup_and_login_api(self):
#     #     response = self.client.post(
#     #         "/api/signup/", {"username": "adi", "password": "dummy"}
#     #     )

#     #     self.assertEqual(response.status_code, 200)
#     #     self.assertIn(
#     #         "login_token", response.json()
#     #     )  # checking if login_Token key is present in response

#     #     response = self.client.post(
#     #         "/api/signup/", {"username": "adi", "password": "dummy"}
#     #     )

#     #     self.assertEqual(response.status_code, 403)
#     #     self.assertEqual(response.json()["message"], "User already exists")

#     #     response = self.client.post(
#     #         "/api/login/", {"username": "adi", "password": "dummy"}
#     #     )

#     #     self.assertEqual(response.status_code, 200)
#     #     # self.assertIn('login_token', response.json())

#     #     response = self.client.post(
#     #         "/api/login/", {"username": "ad", "password": "dummy"}
#         # )

#         # self.assertEqual(response.status_code, 404)
#         # self.assertEqual(response.json()["message"], "Please check the username")

#         # response = self.client.post(
#         #     "/api/login/", {"username": "adi", "password": "dumm"}
#         # )

#         # self.assertEqual(response.status_code, 401)
#         # self.assertEqual(response.json()["message"], "Incorrect Password")


# class TaskAPITestCase(TestCase):

#     def setUp(self):
#         self.client = APIClient()
#         self.user = User.objects.create(username='testuser', password='testpassword')
#         self.client.force_authenticate(user=self.user)
#         # self.user = User.objects.create(username='testuser', password='testpassword')
#         # self.client.force_authenticate(user=self.user) # to ensure user is authenticated

#     def test_create_task_with_valid_data(self):

#         response = self.client.post(
#             "/api/create-task/",
#             {
#                 "title": "first post",
#                 "description": "hey",
#                 "due_date": "20 December 2023",
#                 "status": "OPEN",
#                 "task_tags": [{"tag": "post"}, {"tag": "blog"}],
#             },
#         )
#         task_id = response.json().get("task_id")
#         self.assertEqual(response.status_code, 201)
#         self.assertTrue(Task.objects.filter(id=task_id).exists())
#         self.assertEqual(TaskTag.objects.filter(task_id=task_id).count(), 2)

#     def test_create_task_with_invalid_status(self):
#         response = self.client.post(
#             "/api/create-task/",
#             {
#                 "title": "second post",
#                 "description": "hello",
#                 "due_date": "25 December 2023",
#                 "status": "NOT_OPEN",  # Invalid status
#                 "task_tags": [{"tag": "holiday"}],
#             },
#         )
#         self.assertEqual(response.status_code, 400)
#         self.assertIn("status", response.json())

#     def test_create_task_unauthenticated_user(self):
#         # remove authentication
#         self.client.force_authenticate(user=None)

#         response = self.client.post(
#             "/api/create-task/",
#             {
#                 "title": "Unauthenticated post",
#                 "description": "Unauthenticated access",
#                 "due_date": "30 December 2023",
#                 "status": "OPEN",
#                 "task_tags": [{"tag": "unAuthenticated"}],
#             },
#         )
#         import pdb
#         pdb.set_trace()
#         self.assertNotEqual(response.status_code, 201)
#         self.assertIn("detail", response.json())

# def test_todo_tasks(self):
#     response = self.client.post(
#         "/api/signup/", {"username": "adi", "password": "dummy"}
#     )

#     token = response.json().get("login_token")

#     response = self.client.post(
#         "/api/create-task/",
#         {
#             "title": "first post",
#             "description": "hey",
#             "due_date": "20december",
#             "status": "OPEN",
#             "tags": ["post", "blog"],
#         },
#         HTTP_AUTHORIZATION=token,
#     )

#     task_id = response.json()["task_id"]

#     self.assertEqual(response.status_code, 200)
#     self.assertTrue(Task.objects.filter(id=task_id).exists())

#     response = self.client.post(
#         "/api/create-task/",
#         {
#             "title": "first post",
#             "description": "hey",
#             "due_date": "20december",
#             "status": "NOT_OPEN",
#             "tags": ["post", "blog"],
#         },
#         HTTP_AUTHORIZATION=token,
#     )

#     self.assertEqual(response.status_code, 400)
#     self.assertEqual(response.json()["message"], "Invalid status")

#     response = self.client.get(
#         "/api/task/?id=" + str(task_id), HTTP_AUTHORIZATION=token
#     )

#     self.assertEqual(response.status_code, 200)

#     response = self.client.get("/api/task/?id=" + str(2), HTTP_AUTHORIZATION=token)

#     self.assertEqual(response.status_code, 404)
#     self.assertEqual(response.json()["message"], "No such task")

#     response = self.client.get("/api/all-tasks/", HTTP_AUTHORIZATION=token)

#     self.assertEqual(response.status_code, 200)

#     response = self.client.post(
#         "/api/update-task/?id=" + str(task_id),
#         {
#             "title": "first updated post",
#             "due_date": "21december",
#             "status": "OPEN",
#             "tags": ["post", "blog", "MORE", "fun"],
#         },
#         HTTP_AUTHORIZATION=token,
#     )

#     self.assertEqual(response.status_code, 200)

#     response = self.client.post(
#         "/api/update-task/?id=" + str(12),
#         {
#             "title": "first updated post",
#             "due_date": "21december",
#             "status": "OPEN",
#             "tags": ["post", "blog", "MORE", "fun"],
#         },
#         HTTP_AUTHORIZATION=token,
#     )

#     self.assertEqual(response.status_code, 404)
#     self.assertEqual(response.json()["message"], "No such task")

#     response = self.client.post(
#         "/api/update-task/?id=" + str(task_id),
#         {
#             "title": "first updated post",
#             "due_date": "21december",
#             "status": "OPEN_IN",
#             "tags": ["post", "blog", "MORE", "fun"],
#         },
#         HTTP_AUTHORIZATION=token,
#     )

#     self.assertEqual(response.status_code, 400)
#     self.assertEqual(response.json()["message"], "Invalid status")

#     response = self.client.post(
#         "/api/delete-task/?id=" + str(2), HTTP_AUTHORIZATION=token
#     )

#     self.assertEqual(response.status_code, 404)
#     self.assertEqual(response.json()["message"], "No such task")

#     response = self.client.post(
#         "/api/delete-task/?id=" + str(task_id), HTTP_AUTHORIZATION=token
#     )

#     self.assertEqual(response.status_code, 204)
#     self.assertFalse(Task.objects.filter(id=task_id).exists())
