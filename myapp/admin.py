from django.contrib import admin
from .models import CustomUser,Car,Booking
# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Car)
admin.site.register(Booking)