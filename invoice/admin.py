from django.contrib import admin
from .models import Invoice

@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'organization', 'start_period', 'end_period', 'total_amount', 'status')
    list_filter = ('status', 'start_period', 'organization')
    search_fields = ('organization__name',)
    date_hierarchy = 'start_period'

