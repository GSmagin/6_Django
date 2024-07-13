from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from .models import CustomUser


class UserRegisterForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = ('email', 'password1', 'password2')


class UpdateUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'avatar', 'phone_number', 'country')


