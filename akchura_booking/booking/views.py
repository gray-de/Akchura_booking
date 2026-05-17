from django.shortcuts import render
from django.views.generic import ListView, TemplateView
from .models import Cottage


class IndexListView(ListView):
    model = Cottage
    template_name = 'booking/index.html'
    context_object_name = 'cottages'


class TestTemplateView(TemplateView):
    template_name = 'booking/test.html'
