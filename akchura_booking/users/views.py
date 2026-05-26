from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views.generic import DetailView, UpdateView
from django.contrib.auth.views import LoginView
from django.contrib.auth import get_user_model
from django import forms
from .forms import UserUpdateForm
from django.contrib.auth.mixins import LoginRequiredMixin
from booking.models import Comment, Booking
from django.db.models import Prefetch

User = get_user_model()


class ProfileDetailView(DetailView):
    model = get_user_model()
    template_name = 'users/profile.html'
    slug_field = 'username'
    slug_url_kwarg = 'username'

    # def get_object(self, queryset=None):
    #     obj = get_object_or_404(User.objects.prefetch_related('user_comments', 'user_bookings', 'user_comments__cottage'),
    #                             username=self.kwargs.get('username'))
    #     return obj

    def get_object(self, queryset=None):
        # Предзагружаем комментарии с автором (user) и коттеджем
        comments_qs = Comment.objects.select_related('client', 'cottage')
        # Предзагружаем бронирования с коттеджем (client не нужен, т.к. это тот же пользователь)
        bookings_qs = Booking.objects.select_related('cottage')

        user = get_object_or_404(
            self.model.objects.prefetch_related(
                Prefetch('user_comments', queryset=comments_qs),
                Prefetch('user_bookings', queryset=bookings_qs),
            ),
            username=self.kwargs['username']
        )
        return user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = self.object
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
