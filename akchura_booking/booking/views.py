from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import (ListView, TemplateView, DetailView,
                                  CreateView, UpdateView, DeleteView)
from .models import Cottage, Booking, Comment
from .forms import BookingForm, CommentCreationForm, CommentEditForm
from django import forms
from django.db import models, transaction
from datetime import datetime, time
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin


class IndexListView(ListView):
    model = Cottage
    template_name = 'booking/index.html'
    context_object_name = 'cottages'
    paginate_by = 5


class TestTemplateView(TemplateView):
    template_name = 'booking/test.html'


class CottageDetailView(DetailView):
    model = Cottage
    template_name = 'booking/detail.html'
    context_object_name = 'cottage'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentCreationForm()
        context['comments'] = self.object.cottage_comments.all()
        return context


class BookingCreateView(LoginRequiredMixin, CreateView):
    model = Booking
    template_name = 'booking/booking_create.html'
    form_class = BookingForm

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['cottage'] = get_object_or_404(Cottage, pk=self.kwargs['cottage_id'])
    #     context['check_in_date']
    #     return context

    @transaction.atomic
    def form_valid(self, form):
        cottage = get_object_or_404(Cottage.objects.select_for_update(),
                                    pk=self.request.POST.get('cottage'),
                                    is_active=True)
        check_in_date_str = self.request.POST.get('check_in_date')
        check_out_date_str = self.request.POST.get('check_out_date')
        check_in_date = timezone.make_aware(datetime.combine(datetime.strptime(
            check_in_date_str, '%Y-%m-%d'), time.min))
        check_out_date = timezone.make_aware(datetime.combine(datetime.strptime(
            check_out_date_str, '%Y-%m-%d'), time.min))
        people_number = int(self.request.POST.get('people_number'))

        if people_number > cottage.capacity:
            form.add_error(
                None, f'Домик не может вместить больше {cottage.capacity} человек')
            return self.form_invalid(form)
        # conflict = Booking.objects.filter(
        #     ~models.Q(status='cancelled'),
        #     cottage=cottage,
        #     check_in_date__lt=check_out_date,
        #     check_out_date__gt=check_in_date
        # )

        # if conflict.exists():
        #     form.add_error(None, (f'Этот домик уже забронирован на даты '
        #                           f'с {conflict.first().check_in_date.date()} '
        #                           f'до {conflict.first().check_out_date.date()}'))
        #     return self.form_invalid(form)

        if not cottage.is_available_for_guests(check_in_date, check_out_date, people_number):
            form.add_error(None, 'На эти даты недостаточно свободных мест')
            return self.form_invalid(form)

        form.instance.cottage = cottage
        form.instance.check_in_date = check_in_date
        form.instance.check_out_date = check_out_date
        form.instance.people_number = people_number
        form.instance.client = self.request.user

        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('booking:homepage')


def create_comment(request, pk):
    cottage = get_object_or_404(Cottage, pk=pk)
    form = CommentCreationForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.client = request.user
        comment.cottage = cottage
        comment.save()
    return redirect('booking:cottage', pk=cottage.pk)


class CommentMixin:
    model = Comment
    template_name = 'booking/comment_edit.html'

    def get_object(self, queryset=None):
        pk = self.kwargs.get('pk')
        comment_id = self.kwargs.get('comment_id')
        return get_object_or_404(self.get_queryset(), cottage=pk, pk=comment_id)

    def get_success_url(self):
        return reverse('booking:cottage', kwargs={'pk': self.kwargs.get('pk')})


class CommentUpdateView(CommentMixin, UpdateView):
    form_class = CommentEditForm


class CommentDeleteView(CommentMixin, DeleteView):
    pass
