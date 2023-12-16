from rest_framework import serializers
from todo.models import User, Task, TaskTag
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import make_password, check_password
import uuid

class UserSignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "password"]

    def validate(self, data):
        username = data.get("username")
        if User.objects.filter(username = username).exists():
            raise serializers.ValidationError("User already exists")
        return data

    def create(self, validated_data):
        validated_data["password"] = make_password(validated_data["password"])
        validated_data["login_token"] = str(uuid.uuid4())
        return super().create(validated_data)


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        username = data.get("username")
        password = data.get("password")

        user = User.objects.filter(username=username).first()
        if not user:
            raise serializers.ValidationError({"username": "User does not exist"})
        if not check_password(password, user.password):
            raise serializers.ValidationError({"password": "Incorrect Password"})
        
        return data
    
# class UserLoginSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ["username", "password"]

#     def validate(self, data):
#         username = data.get("username")
#         password = data.get("password")
        
#         user = User.objects.filter(username = username).first()
#         if not user:
#             raise serializers.ValidationError("User does not exist")
#         if not check_password(password, user.password):
#             raise serializers.ValidationError("Incorrect Password")
#         return data
    
class TaskTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskTag
        fields = ['tag']

    def create(self, validated_data):
        task = self.context.get('task')
        user = self.context.get('user')
        return TaskTag.objects.create(task=task, user=user, **validated_data)


class TaskSerializer(serializers.ModelSerializer):
    task_tags = TaskTagSerializer(many=True, required=False)

    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'due_date', 'status', 'task_tags', 'user']
        extra_kwargs = {'user': {'write_only': True}}

    def create(self, validated_data):
        tags_data = validated_data.pop('task_tags', [])
        task = Task.objects.create(**validated_data)

        for tag_data in tags_data:
            TaskTag.objects.create(task=task, **tag_data)

        return task


    
    # def get_task_tags(self, obj):
    #     tags = TaskTag.objects.filter(task=obj)
    #     return [tag.tag for tag in tags]


class TaskRetrievalSerializer(serializers.Serializer):
    id = serializers.IntegerField()

    def validate_id(self, value):
        if not Task.objects.filter(id=value).exists():
            raise serializers.ValidationError("No such task")
        return value

class AllTasksRetrievalSerializer(serializers.Serializer):
    def validate(self, data):
        user = self.context['request'].user
        if not Task.objects.filter(user=user).exists():
            raise serializers.ValidationError("No tasks found for the user")
        return data

