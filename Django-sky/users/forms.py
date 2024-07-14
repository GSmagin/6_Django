from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm, PasswordResetForm
from .models import CustomUser

from .mixins import StyleFormMixin


class StyledAuthenticationForm(StyleFormMixin, AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'form-control custom-username-class mt-2',
            'placeholder': 'Адрес электронной почты',
            'type': 'email',  # Примените тип email для правильной валидации
        })
        self.fields['password'].widget.attrs.update({
            'class': 'form-control custom-username-class mt-2',
            'placeholder': 'Пароль',
        })

    class Meta:
        model = CustomUser
        fields = ['email', 'password']


class StyledPasswordResetForm(StyleFormMixin, PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({
            'class': 'form-control custom-username-class mt-2',
            'placeholder': 'Адрес электронной почты',
            'type': 'email',
        })


class ProfileUpdateForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['email', 'avatar', 'country', 'phone_number']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({
            'placeholder': 'email',
        })
        self.fields['avatar'].widget.attrs.update({
            'placeholder': 'Адрес электронной почты',
            'type': 'Аватар',  # Примените тип email для правильной валидации
        })
        self.fields['country'].widget.attrs.update({
            'placeholder': 'Страна',
        })
        self.fields['phone_number'].widget.attrs.update({
            'placeholder': 'Номер телефона',
        })


class UserRegisterForm(StyleFormMixin, UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['email', 'password1', 'password2']


class UpdateUserChangeForm(StyleFormMixin, UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'avatar', 'phone_number', 'country')


