from django.db import models
from django.conf import settings

class Booking(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='bookings')
    desk = models.ForeignKey('spaces.Desk', on_delete=models.CASCADE, related_name='bookings')
    invoice = models.ForeignKey('invoice.Invoice', on_delete=models.SET_NULL,
                                null=True, blank=True, related_name='bookings')
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    class BookingStatus(models.TextChoices):
        PENDING = 'pending', 'Очікує'
        CONFIRMED = 'confirmed', 'Підтверджено'
        CANCELLED = 'cancelled', 'Скасовано'
        FINISHED = 'finished', 'Завершено'

    status = models.CharField(max_length=20, choices=BookingStatus.choices, default=BookingStatus.PENDING)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Замовлення №{self.id} - Юзер: {self.user} (Стіл :{self.desk.number})"
