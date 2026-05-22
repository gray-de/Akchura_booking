from django.shortcuts import render
from django.urls import reverse
from django.views.generic import DetailView
from django.contrib.auth.views import LoginView
from django.contrib.auth import get_user_model


class ProfileDetailView(DetailView):
    model = get_user_model()
    template_name = 'users/profile.html'
    slug_field = 'username'
    slug_url_kwarg = 'username'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = self.object
        return context


class CustomLoginView(LoginView):
    def get_success_url(self):
        return reverse('booking:homepage')
