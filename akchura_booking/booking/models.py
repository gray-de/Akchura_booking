from django.db import models
from django.core.validators import MinValueValidator


class Cottage(models.Model):
    name = models.CharField(max_length=50, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    capacity = models.PositiveSmallIntegerField(verbose_name='Вместимость',
                                                validators=[MinValueValidator(1)])
    price = models.DecimalField(verbose_name='Цена',
                                max_digits=8,
                                decimal_places=2)
    photo = models.ImageField(upload_to='cottages/',
                              verbose_name='Фото', blank=True)
    is_active = models.BooleanField(default=True,
                                    verbose_name='Доступность для брони')

    class Meta:
        verbose_name = 'Домик'
        verbose_name_plural = 'Домики'
        ordering = ['name',]
