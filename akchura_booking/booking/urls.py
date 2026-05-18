from django.urls import path
from booking import views


app_name = 'booking'

urlpatterns = [
    path('', views.IndexListView.as_view(), name='homepage'),
    path('cottages/', views.TestTemplateView.as_view()),
    path('cottages/<int:pk>/',
         views.CottageDetailView.as_view(),
         name='cottage'),
    path('booking/create/', views.BookingCreateView.as_view(), name='booking_create')
]
