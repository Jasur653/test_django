from django.db import models
from django.utils.translation import gettext_lazy as _
from products.models import Product


class Customer(models.Model):
    name = models.CharField(_("Customer Name"), max_length=200)
    email = models.EmailField(_("Email"), blank=True, null=True)
    phone = models.CharField(_("Phone"), max_length=20)
    address = models.TextField(_("Address"))
    created_at = models.DateTimeField(_("Created At"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated At"), auto_now=True)

    class Meta:
        verbose_name = _("Customer")
        verbose_name_plural = _("Customers")

    def __str__(self):
        return self.name


class Order(models.Model):
    STATUS_CHOICES = [
        ('RECEIVED', _('Received')),
        ('PROCESSING', _('Processing')),
        ('SHIPPED', _('Shipped')),
        ('DELIVERED', _('Delivered')),
        ('CANCELLED', _('Cancelled')),
    ]

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="orders", verbose_name=_("Customer"))
    order_number = models.CharField(_("Order Number"), max_length=20, unique=True)
    status = models.CharField(_("Status"), max_length=20, choices=STATUS_CHOICES, default='RECEIVED')
    total_amount = models.DecimalField(_("Total Amount"), max_digits=10, decimal_places=2)
    notes = models.TextField(_("Notes"), blank=True, null=True)
    created_at = models.DateTimeField(_("Created At"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated At"), auto_now=True)

    class Meta:
        verbose_name = _("Order")
        verbose_name_plural = _("Orders")
        ordering = ['-created_at']

    def __str__(self):
        return f"Order #{self.order_number}"

    def save(self, *args, **kwargs):
        # Generate order number if not provided
        if not self.order_number:
            last_order = Order.objects.order_by('-id').first()
            if last_order:
                last_id = last_order.id
            else:
                last_id = 0
            self.order_number = f"ORD-{last_id + 1:06d}"

        super().save(*args, **kwargs)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items", verbose_name=_("Order"))
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name=_("Product"))
    quantity = models.PositiveIntegerField(_("Quantity"))
    price = models.DecimalField(_("Price"), max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = _("Order Item")
        verbose_name_plural = _("Order Items")

    def __str__(self):
        return f"{self.product.name} ({self.quantity}) - {self.order.order_number}"

    @property
    def subtotal(self):
        return self.price * self.quantity