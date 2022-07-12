import json

import requests
from django.contrib import messages
from django.contrib.auth import authenticate
from django.shortcuts import render, redirect
from rest_framework import generics
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from .forms import UserRegisterForm, UserLoginForm, UserUpdateForm
from .serializers import UserSerializer
from .utils import get_tokens_for_user


class UserRegister(generics.CreateAPIView):
    """
    User Register View returning:
    - GET request - return HTML page with Form (Register Form)
    - POST request - retrieve User data, creates new User and return Login page
    """

    renderer_classes = [TemplateHTMLRenderer]
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        return Response(template_name='budget_django/register.html', data={
            "form": UserRegisterForm,
        })

    def post(self, request, *args, **kwargs):
        form_data = {
            "username": request.data.get("username"),
            "email": request.data.get("email"),
            "password": request.data.get("password1"),
            "password2": request.data.get("password2")
        }
        serializer_class = self.serializer_class()
        validated_data = serializer_class.validate(form_data)
        try:
            serializer_class.create(validated_data)
        except Exception as e:
            messages.add_message(request, messages.INFO, "sdcsdc")

        return Response(template_name='budget_django/login.html', data={
            "form": UserRegisterForm(),
            "messages": messages
        })


class UserProfile(APIView):
    """
    User Profile View returning:
    - GET request - return HTML page with Profile of User and
        User Update Form and Profile Update Form
    - POST request - retrieve data, updates User and user`s Profile

    Also checking that user in authenticated and token is valid or
        redirect to logout view
    """

    renderer_classes = [TemplateHTMLRenderer]

    def post(self, request, *args, **kwargs):
        token = request.COOKIES.get('token')
        user = user_from_token(token)
        u_form = UserUpdateForm(request.POST, instance=user)
        if u_form.is_valid():
            u_form.save()
            messages.success(request, 'Account has been updated')
            return redirect('profile')

    def get(self, request, *args, **kwargs):
        token = refresh_token_or_redirect(request)

        if not isinstance(token, str):
            return redirect('logout')

        user = user_from_token(token=token)

        u_form = UserUpdateForm(instance=user)
        p_form = ProfileUpdateForm(instance=user)
        context = {
            "user": {
                "image": user.profile.image
            },
            'u_form': u_form,
            'p_form': p_form,
        }

        return render(request, 'users/profile.html', context)


class LoginView(APIView):
    headers = {
        'Content-Type': 'application/json',
    }

    """
    User Login View returning:
    - GET request - return HTML page with User Login Form
    - POST request - retrieve data, authenticate User, create 'token' and 'refresh' and set them as cookie

    """

    renderer_classes = [TemplateHTMLRenderer]

    def get(self, request, *args, **kwargs):
        return Response(template_name='budget_django/login.html', data={
            "form": UserLoginForm
        })

    def post(self, request, *args, **kwargs):
        user = authenticate(username=request.data['username'],
                            password=request.data['password'])
        if user:
            pair_tokens = get_tokens_for_user(
                user)  # creating tokens for user authentication

            result = Response(
                template_name='budget_django/home.html',
                headers=self.headers,
            )

            result.set_cookie("refresh", pair_tokens["refresh"])
            result.set_cookie("token", pair_tokens["token"])
            return result

        else:
            messages.error(request,
                           "Cannot find user with this email and password")
            return Response(template_name='budget_django/login.html', data={
                "form": UserLoginForm
            })


class LogoutView(APIView):
    """
    User Logout View returning:
    - GET request - delete cookie and return Logout HTML page

    """

    renderer_classes = [TemplateHTMLRenderer]

    def get(self, request, *args, **kwargs):
        response = Response(template_name='budget_django/logout.html', data={
            'user': None
        })
        response.delete_cookie('refresh')
        response.delete_cookie('token')

        return response
