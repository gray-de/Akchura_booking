from django.urls import path
from booking import views


app_name = 'booking'

urlpatterns = [
    path('', views.IndexListView.as_view(), name='homepage'),
    path('cottages/', views.TestTemplateView.as_view()),
    path('cottages/<int:pk>/comment/create/',
         views.create_comment, name='create_comment'),
    path('cottages/<int:pk>/comment/<int:comment_id>/edit/',
         views.CommentUpdateView.as_view(), name='edit_comment'),
    path('cottages/<int:pk>/comment/<int:comment_id>/delete/',
         views.CommentDeleteView.as_view(), name='delete_comment'),
    path('cottages/<int:pk>/',
         views.CottageDetailView.as_view(),
         name='cottage'),
    path('booking/create/', views.BookingCreateView.as_view(),
         name='booking_create')
]
