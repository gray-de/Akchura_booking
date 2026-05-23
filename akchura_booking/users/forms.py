from django import forms
from .models import MyUser
from django.contrib.auth.forms import UserCreationForm
from .validators import validate_capitalized
from django.contrib.auth import get_user_model

User = get_user_model()


class UserFormMixin:
    first_name = forms.CharField(
        required=True,
        max_length=25,
        validators=[validate_capitalized],
        label='Имя'
    )

    last_name = forms.CharField(
        required=True,
        max_length=50,
        validators=[validate_capitalized],
        label='Фамилия'
    )


class CustomUserCreationForm(UserCreationForm, UserFormMixin):
    class Meta(UserCreationForm.Meta):
        model = MyUser
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "telephone",
        ]


class UserUpdateForm(forms.ModelForm, UserFormMixin):
    class Meta:
        model = MyUser
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "telephone",
        ]
