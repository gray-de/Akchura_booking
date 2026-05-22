from django.db import models
from booking.validators import phone_regex
from django.contrib.auth.models import AbstractUser


class MyUser(AbstractUser):
    telephone = models.CharField(
        validators=[phone_regex],
        max_length=17,
        unique=True,
        blank=False,
        verbose_name='Номер телефона'
    )
