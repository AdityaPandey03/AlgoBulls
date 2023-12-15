from django.test import TestCase
from todo.models import *

class UserAPITestCase(TestCase):
    
    def test_signup_and_login_api(self):

        response = self.client.post(
            "/api/signup/", {"username" : "adi", "password" : "dummy"}
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn('login_token', response.json()) # checking if login_Token key is present in response

        response = self.client.post(
            "/api/signup/", {"username" : "adi", "password" : "dummy"}
        )

        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json()["message"], "User already exists")

        response = self.client.post(
            "/api/login/", {"username" : "adi", "password" : "dummy"}
        )

        self.assertEqual(response.status_code, 200)
       # self.assertIn('login_token', response.json())

        response = self.client.post(
            "/api/login/", {"username" : "ad" , "password" : "dummy"}
        )
        
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json()["message"], "Please check the username")

        response = self.client.post(
            "/api/login/", {"username" : "adi" , "password" : "dumm"}
        )

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json()["message"], "Incorrect Password")


class TaskAPITestCase(TestCase):

    def test_todo_tasks(self):

        response = self.client.post(
            "/api/signup/", {"username" : "adi", "password" : "dummy"}
        )

        token = response.json().get('login_token')

        response = self.client.post(
            "/api/create-task/", {"title" : "first post", "description" : "hey", "due_date" : "20december" , "status": "OPEN" , "tags" : ['post', 'blog']}, HTTP_AUTHORIZATION = token
        )

        task_id = response.json()["task_id"]

        self.assertEqual(response.status_code, 200)
        self.assertTrue(Task.objects.filter(id = task_id).exists())


        response = self.client.post(
            "/api/create-task/", {"title" : "first post", "description" : "hey", "due_date" : "20december" , "status": "NOT_OPEN" , "tags" : ['post', 'blog']}, HTTP_AUTHORIZATION = token
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["message"], "Invalid status")

        response = self.client.get(
            "/api/task/?id=" + str(task_id), HTTP_AUTHORIZATION = token
        )

        self.assertEqual(response.status_code, 200)

        response = self.client.get(
            "/api/task/?id=" + str(2), HTTP_AUTHORIZATION = token
        )

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json()["message"], "No such task")


        response = self.client.get(
            "/api/all-tasks/", HTTP_AUTHORIZATION = token
        )

        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            "/api/update-task/?id=" + str(task_id), {"title" : "first updated post", "due_date" : "21december" , "status": "OPEN" , "tags" : ['post', 'blog','MORE','fun']}, HTTP_AUTHORIZATION = token
        )

        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            "/api/update-task/?id=" + str(12), {"title" : "first updated post", "due_date" : "21december" , "status": "OPEN" , "tags" : ['post', 'blog','MORE','fun']}, HTTP_AUTHORIZATION = token
        )

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json()["message"], "No such task")

        response = self.client.post(
            "/api/update-task/?id=" + str(task_id), {"title" : "first updated post", "due_date" : "21december" , "status": "OPEN_IN" , "tags" : ['post', 'blog','MORE','fun']}, HTTP_AUTHORIZATION = token
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["message"], "Invalid status")

        response = self.client.post(
            "/api/delete-task/?id=" + str(2), HTTP_AUTHORIZATION = token
        )

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json()["message"], "No such task")


        response = self.client.post(
            "/api/delete-task/?id=" + str(task_id), HTTP_AUTHORIZATION = token
        )

        self.assertEqual(response.status_code, 204)
        self.assertFalse(Task.objects.filter(id = task_id).exists())














    

























        





        












