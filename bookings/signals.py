from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

from .models import Booking
from invoice.models import Invoice

@receiver(post_save, sender=Booking)
def create_invoice_for_booking(sender, instance, created, **kwargs):
    if created:
        org = instance.user.organization

        invoice, invoice_created = Invoice.objects.get_or_create(
            organization=org,
            status=Invoice.InvoiceStatus.DRAFT,
            defaults={
                'start_period': timezone.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0),  # Початок місяця
                'end_period': timezone.now(),  # Буде оновлюватися
                'total_amount': 0
            }
        )
        instance.invoice = invoice
        Booking.objects.filter(pk=instance.pk).update(invoice=invoice)
        invoice.total_amount += instance.total_price
        invoice.end_period = max(invoice.end_period, instance.end_time)
        invoice.save()
