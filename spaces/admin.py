from django.contrib import admin
from .models import Organization, Office, Room, Desk

@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'is_active')
    search_fields = ('name',)
    list_filter = ('is_active',)

@admin.register(Office)
class OfficeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'organization', 'city', 'is_active')
    search_fields = ('name', 'city')
    list_filter = ('organization', 'city', 'is_active')

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'office', 'room_type', 'capacity', 'is_active')
    search_fields = ('name',)
    list_filter = ('room_type', 'office', 'is_active')

@admin.register(Desk)
class DeskAdmin(admin.ModelAdmin):
    list_display = ('id', 'number', 'room', 'price_per_hour', 'is_active')
    search_fields = ('number',)
    list_filter = ('room__office', 'room', 'is_active')
