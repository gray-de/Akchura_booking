from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, TemplateView, DetailView, CreateView
from .models import Cottage, Booking
from .forms import BookingForm
from django import forms


class IndexListView(ListView):
    model = Cottage
    template_name = 'booking/index.html'
    context_object_name = 'cottages'


class TestTemplateView(TemplateView):
    template_name = 'booking/test.html'


class CottageDetailView(DetailView):
    model = Cottage
    template_name = 'booking/detail.html'
    context_object_name = 'cottage'


class BookingCreateView(CreateView):
    model = Booking
    template_name = 'booking/booking_create.html'
    form_class = BookingForm

    def get_success_url(self):
        return reverse_lazy('booking:homepage')
