from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from categories.models import Category


class CategoryForm(forms.ModelForm):
    """
    Form for creating Category model
    """

    class Meta:
        model = Category
        fields = '__all__'

# class UserUpdateForm(forms.ModelForm):
#     """
#     Form for updating User model
#     """
#
#     email = forms.EmailField
#
#     class Meta:
#         model = User
#         fields = ['username', 'email']
#
#
# class UserLoginForm(forms.ModelForm):
#     """
#     Form for login User model
#     """
#
#     password = forms.CharField(
#         widget=forms.PasswordInput
#     )
#
#     class Meta:
#         model = User
#         fields = ['username', 'password']
