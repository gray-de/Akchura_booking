from django.urls import path
from users import views


app_name = 'users'

urlpatterns = [
    path('profile/<slug:username>/',
         views.ProfileDetailView.as_view(), name='profile'),

    path('edit_profile/',
         views.ProfileUpdateView.as_view(), name='edit_profile'),
]
