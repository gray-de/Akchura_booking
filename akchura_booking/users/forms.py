from django import forms
from .models import MyUser


class CustomUserCreationForm(forms.ModelForm):
    class Meta:
        model = MyUser
        fields = [
            "username",
            "password",
            "first_name",
            "last_name",
            "email",
            "telephone",
        ]
