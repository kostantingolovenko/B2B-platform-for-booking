from django.db import models

class Payment(models.Model):
    invoice = models.ForeignKey('invoice.Invoice', on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=20, decimal_places=2)

    class PaymentStatus(models.TextChoices):
        IN_PROGRESS = 'in progress', 'В обробці'
        SUCCESSFUL = 'successful', 'Успішно'
        ERROR = 'error', 'Помилка'
        REFUND = 'refund', 'Повернення коштів'

    status = models.CharField(max_length=20, choices=PaymentStatus.choices,
                              default=PaymentStatus.IN_PROGRESS)

    stripe_payment_intent_id = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        unique=True,
        db_index=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Оплата №{self.id} на суму {self.amount} грн'