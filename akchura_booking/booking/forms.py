from .models import Booking
from django import forms


class BookingForm(forms.ModelForm):

    class Meta:
        model = Booking
        fields = ("cottage", "people_number",
                  "check_in_date", "check_out_date",
                  "telephone_number")
