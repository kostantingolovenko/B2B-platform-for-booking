from django.contrib import admin
from .models import Booking

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'desk', 'start_time', 'end_time', 'status', 'total_price')
    list_filter = ('status', 'start_time', 'end_time')
    search_fields = ('user__username', 'desk__number')
    date_hierarchy = 'start_time'