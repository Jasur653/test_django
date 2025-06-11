from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from products.models import Product


class StockMovement(models.Model):
    MOVEMENT_TYPES = [
        ('IN', _('Stock In')),
        ('OUT', _('Stock Out')),
    ]

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="stock_movements",
                                verbose_name=_("Product"))
    movement_type = models.CharField(_("Movement Type"), max_length=3, choices=MOVEMENT_TYPES)
    quantity = models.PositiveIntegerField(_("Quantity"))
    reason = models.TextField(_("Reason"), blank=True, null=True)
    staff = models.ForeignKey(User, on_delete=models.CASCADE, related_name="stock_movements", verbose_name=_("Staff"))
    created_at = models.DateTimeField(_("Created At"), auto_now_add=True)

    class Meta:
        verbose_name = _("Stock Movement")
        verbose_name_plural = _("Stock Movements")
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.get_movement_type_display()} - {self.product.name} ({self.quantity})"

    def save(self, *args, **kwargs):
        # Update product quantity based on movement type
        if self.movement_type == 'IN':
            self.product.quantity += self.quantity
        elif self.movement_type == 'OUT':
            self.product.quantity = max(0, self.product.quantity - self.quantity)

        self.product.save()
        super().save(*args, **kwargs)