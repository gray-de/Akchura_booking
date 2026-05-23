from django.contrib import admin
from .models import Cottage, Booking, Comment
# Register your models here

admin.site.register(Cottage)
admin.site.register(Booking)
admin.site.register(Comment)
