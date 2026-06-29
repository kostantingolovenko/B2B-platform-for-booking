from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'organization', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'organization')
    search_fields = ('username', 'first_name', 'last_name', 'email', 'phone')

    fieldsets = UserAdmin.fieldsets + (
        ('Додаткова інформація (Коворкінг)', {'fields': ('organization', 'phone')}),)
