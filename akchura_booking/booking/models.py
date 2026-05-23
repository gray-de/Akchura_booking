from django.utils import timezone
from django.contrib.auth import get_user_model
from django.db import models
from django.core.validators import MinValueValidator
from .validators import phone_regex
from django.core.exceptions import ValidationError

User = get_user_model()


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

    def is_available_for_guests(self, check_in_date,
                                check_out_date, people_number):
        existing_bookings = self.bookings.exclude(status='cancelled').filter(
            check_in_date__lt=check_out_date,
            check_out_date__gt=check_in_date
        )
        events = []
        for book in existing_bookings:
            events.append((book.check_in_date, book.people_number))
            events.append((book.check_out_date, -book.people_number))

        events.append((check_in_date, people_number))
        events.append((check_out_date, -people_number))

        events.sort(key=lambda x: (x[0], -x[1]))

        current = 0
        max_people = 0

        for _, delta in events:
            current += delta
            if current > max_people:
                max_people = current

        return max_people <= self.capacity

    class Meta:
        verbose_name = 'Домик'
        verbose_name_plural = 'Домики'
        ordering = ['name',]

    def __str__(self):
        return f'Домик {self.name}'


class Booking(models.Model):

    STATUS_CHOICES = [
        ('pending', 'Ожидание подтверждения'),
        ('cancelled', 'Отменено'),
        ('confirmed', 'Подтверждено')
    ]

    cottage = models.ForeignKey(
        Cottage, on_delete=models.CASCADE,
        related_name='bookings',
        verbose_name='Домик')
    people_number = models.SmallIntegerField(
        validators=[MinValueValidator(1)], verbose_name='Кол-во людей')
    check_in_date = models.DateTimeField(verbose_name='Дата заезда')
    check_out_date = models.DateTimeField(verbose_name='Дата выезда')
    client = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name='Пользователь')

    status = models.CharField(choices=STATUS_CHOICES,
                              default='pending', verbose_name='Статус брони')
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='Время создания брони')

    class Meta:
        verbose_name = 'Бронь'
        verbose_name_plural = 'Брони'

    def clean(self):
        if self.check_in_date and self.check_out_date:
            if self.check_in_date >= self.check_out_date:
                raise ValidationError(
                    'Дата заезда должна быть раньше даты выезда.')
            if (self.check_out_date - self.check_in_date).days < 1:
                raise ValidationError('Минимальное бронирование — одна ночь.')

        # 3. Дата заезда не в прошлом (только для новых бронирований)
        if self.pk is None and self.check_in_date and self.check_in_date < timezone.now():
            raise ValidationError('Дата заезда не может быть в прошлом.')
        if self.cottage and self.cottage.capacity is not None and self.people_number is not None:
            if self.cottage.capacity < self.people_number:
                raise ValidationError(
                    f'Коттедж вмещает максимум {self.cottage.capacity} человек, указано {self.people_number}.')

    def __str__(self):
        return (f'Бронь для {self.cottage} '
                f'в количестве {self.people_number} человек')
