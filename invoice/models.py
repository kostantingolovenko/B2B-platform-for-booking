from django.db import models

class Invoice(models.Model):
    organization = models.ForeignKey('spaces.Organization', on_delete=models.CASCADE, related_name='invoices')
    start_period = models.DateTimeField()
    end_period = models.DateTimeField()
    total_amount = models.DecimalField(max_digits=20, decimal_places=2)

    class InvoiceStatus(models.TextChoices):
        DRAFT = 'draft', 'Послуги накопичуються'
        ISSUED = 'issued', 'Очікування оплати)'
        PAID = 'paid', 'Оплачено'
        OVERDUE = 'overdue', 'Протерміновано'

    status = models.CharField(max_length=20, choices=InvoiceStatus.choices, default=InvoiceStatus.DRAFT)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Інвойс {self.id} для {self.organization.name} ({self.total_amount})"