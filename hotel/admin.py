from django.contrib import admin
from .models import Room, Booking, Payment, UserProfile, ContactMessage

# Register your models here.
admin.site.register(Room)
admin.site.register(Booking)
admin.site.register(Payment)
admin.site.register(UserProfile)
admin.site.register(ContactMessage)
