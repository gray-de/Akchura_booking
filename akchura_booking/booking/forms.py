from .models import Booking
from django import forms
from django.utils import timezone


class BookingForm(forms.ModelForm):

    class Meta:
        model = Booking
        fields = ("cottage", "people_number",
                  "check_in_date", "check_out_date",
                  "telephone_number")
        widgets = {
            'check_in_date': forms.DateInput(attrs={'type': 'date'}),
            'check_out_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        check_in_date = cleaned_data.get('check_in_date')
        check_out_date = cleaned_data.get('check_out_date')
        people_number = cleaned_data.get('people_number')
        cottage = cleaned_data.get('cottage')

        if check_in_date and check_out_date:
            if check_in_date > check_out_date:
                self.add_error('check_out_date',
                               'Дата заезда должна быть раньше даты выезда.')
            if (check_out_date - check_in_date).days < 1:
                self.add_error('check_out_date',
                               'Минимальное бронирование — одна ночь.')

        # 3. Дата заезда не в прошлом (только для новых бронирований)
        if check_in_date and check_in_date < timezone.now():
            self.add_error('check_in_date',
                           'Дата заезда не может быть в прошлом')

        if cottage.capacity < people_number:
            self.add_error(
                'people_number', f'Количество людей не может быть больше вместимости домика({cottage.capacity}).')
