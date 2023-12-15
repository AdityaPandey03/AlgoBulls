import uuid
from django.shortcuts import render
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from todo.models import *
from rest_framework.status import HTTP_401_UNAUTHORIZED
from todo.helper import CustomAuthentication
from rest_framework import exceptions
from django.core.exceptions import ObjectDoesNotExist


class UserViewSet(ViewSet):

    def user_signup(self, request):

        input_username = request.data.get("username")
        input_password = request.data.get("password")

        if User.objects.filter(username = input_username).exists():
            return Response(data = {"message" : "User already exists"}, status = 403)
        
        user = User.objects.create(
            username = input_username,
            password = input_password,
            login_token = str(uuid.uuid4())
        )

        return Response(data = {"message" : f"{input_username}, you are on board!", "login_token" : user.login_token}, status = 200)
    
    def user_login(self, request):

        input_username = request.data.get("username")
        input_password = request.data.get("password")

        if not User.objects.filter(username = input_username).exists():
            return Response(data = {"message" : "Please check the username"} , status = 404)
        
        user = User.objects.filter(username = input_username).get()

        if user.password != input_password:
            return Response(data = {"message" : "Incorrect Password"}, status = 401)
        
        new_token = str(uuid.uuid4())
        user.login_token = new_token
        user.save()

        return Response(data = {"message" : "Login successful"}, status = 200)
    
class TaskViewSet(ViewSet):

    authentication_classes = [CustomAuthentication]
    # FIRST,  user is authenticated based on token based authentication, if the user is authenticated, then the request will be passed to the viewSet

    def create_task(self, request):

        input_user_id = request.user.id
        input_title = request.data.get("title")
        input_description = request.data.get("description")
        input_due_date = request.data.get("due_date")
        input_status = request.data.get("status")
        input_tags = request.data.get("tags", [])

        valid_status = [choice[0] for choice in Task.STATUS_CHOICES] 

        if input_status is None:
            input_status = "OPEN"

        if input_status not in valid_status:
            return Response(data = {"message" : "Invalid status"}, status = 400)

        task = Task.objects.create(
            user_id = input_user_id,
            title = input_title,
            description = input_description,
            due_date = input_due_date,
            status = input_status
        )

        for tag in input_tags: # managing the tags, storing them in a separate table
            TaskTag.objects.create(
                user_id = input_user_id,
                task_id = task.id,
                tag = tag
            )
        
        return Response(data = {"message": "Task created successfully", "task_id": task.id}, status = 200)

    
    def get_task(self, request):

        input_user_id = request.user.id
        input_task_id = request.GET.get("id")
        
        if not Task.objects.filter(id = input_task_id).exists():
            return Response(data = {"message" : "No such task"}, status = 404)

        task = Task.objects.filter(id = input_task_id).get()

        if task.user_id != input_user_id:
            return Response(data = {"message" : "Not authorized to access this task"}, status = 401)
        
        task_tags = TaskTag.objects.filter(task_id = input_task_id, user_id = input_user_id).all()
        tags = [x.tag for x in task_tags]

        return Response(data = {
            "id" : task.id,
            "title" : task.title,
            "description" : task.description,
            "due_date" : task.due_date,
            "status" : task.status,
            "tags" : tags
        }, status = 200)


    def get_all_tasks(self, request):

        input_user_id = request.user.id

        if not Task.objects.filter(user_id = input_user_id).exists():
            return Response(data = {"message" : "No such user"}, status = 404)

        tasks = Task.objects.filter(user_id = input_user_id)
        all_tasks = []

        for task in tasks:
            
            task_tags = TaskTag.objects.filter(user_id = input_user_id, task_id=task.id).all()
            tags = [x.tag for x in task_tags]

            all_tasks.append({
                "id" : task.id,
                "title" : task.title,
                "description" : task.description,
                "due_date" : task.due_date,
                "status" : task.status,
                "tags" : tags
            })

        return Response(data = {"message" : all_tasks}, status = 200)
    
    def delete_task(self, request):

        input_user_id = request.user.id
        input_task_id = request.GET.get("id")

        if not Task.objects.filter(id = input_task_id).exists():
            return Response(data = {"message" : "No such task"}, status = 404)
        
        task = Task.objects.filter(id = input_task_id).get()

        if task.user_id != input_user_id:
            return Response(data = {"message" : "Not authorized to delete this task"}, status = 401)    
        
        task.delete()
        return Response(data={f"message: Task {input_task_id} deleted successfully"}, status=204) 
    

    def update_task(self, request):

        input_user_id = request.user.id
        input_task_id = request.GET.get("id")
        input_title = request.data.get("title")
        input_description = request.data.get("description")
        input_due_date = request.data.get("due_date")
        input_status = request.data.get("status")
        input_tags = request.data.get("tags", [])

        if not Task.objects.filter(id = input_task_id).exists():
            return Response(data = {"message" : "No such task"}, status = 404)
        
        task = Task.objects.filter(id = input_task_id).get()

        if task.user_id != input_user_id:
            return Response(data = {"message" : "Not authorized to update this task"}, status = 401)
        
        valid_status = [choice[0] for choice in Task.STATUS_CHOICES] 

        if input_status not in valid_status:
            return Response(data = {"message" : "Invalid status"}, status = 400)

        
        if input_title is not None:
            task.title = input_title
        if input_description is not None:
            task.description = input_description
        if input_due_date is not None:
            task.due_date = input_due_date
        if input_status is not None:
            task.status = input_status

        task.save()

        TaskTag.objects.filter(task_id = input_task_id, user_id = input_user_id).delete()

        for tag in input_tags: 
            TaskTag.objects.create(
                user_id = input_user_id,
                task_id = task.id,
                tag = tag
            )
        
        return Response(data = {f"message : Task {input_task_id} updated successfully"}, status = 200)

    


    

        


            





        

