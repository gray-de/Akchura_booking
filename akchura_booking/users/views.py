from django.shortcuts import render
from django.urls import reverse
from django.views.generic import DetailView, UpdateView
from django.contrib.auth.views import LoginView
from django.contrib.auth import get_user_model
from django import forms
from .forms import UserUpdateForm
from django.contrib.auth.mixins import LoginRequiredMixin
from booking.models import Comment

User = get_user_model()


class ProfileDetailView(DetailView):
    model = get_user_model()
    template_name = 'users/profile.html'
    slug_field = 'username'
    slug_url_kwarg = 'username'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = self.object
        context['comments'] = self.object.user_comments.all()
        if self.object == self.request.user:
            context['bookings'] = self.object.user_bookings.all()

        return context


class CustomLoginView(LoginView):
    def get_success_url(self):
        return reverse('booking:homepage')


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    template_name = 'users/edit_profile.html'
    form_class = UserUpdateForm

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse('users:profile', args=[self.request.user.username])
