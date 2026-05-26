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

    image = models.ImageField(
        upload_to='profile_pictures', verbose_name='Картинка профиля',
        blank=True, null=True)

    def __str__(self):
        return self.username
