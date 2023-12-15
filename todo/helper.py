from todo.models import User
from rest_framework import exceptions
from rest_framework import authentication
from rest_framework.status import HTTP_401_UNAUTHORIZED
from rest_framework.response import Response


def get_user_from_login_token(input_login_token):
    return User.objects.filter(login_token=input_login_token).first()


# so here, what happens is filter returns a list of user instances, using first() we get the user instance


class CustomAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        input_login_token = request.META.get("HTTP_AUTHORIZATION")
        user = get_user_from_login_token(input_login_token)

        if User is None:
            raise exceptions.AuthenticationFailed("No such user")
        return (user, None)


# so, in authenticate method, convention of using authenticate method is that a two tuple is passed, first ele is authenticated user and the other is any additional info
