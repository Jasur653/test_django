from django.db import models
from django.utils.translation import gettext_lazy as _
from products.models import Product


class Supplier(models.Model):
    name = models.CharField(_("Supplier Name"), max_length=200)
    contact_person = models.CharField(_("Contact Person"), max_length=200)
    email = models.EmailField(_("Email"), blank=True, null=True)
    phone = models.CharField(_("Phone"), max_length=20)
    address = models.TextField(_("Address"))
    products = models.ManyToManyField(Product, related_name="suppliers", blank=True, verbose_name=_("Products"))
    created_at = models.DateTimeField(_("Created At"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated At"), auto_now=True)

    class Meta:
        verbose_name = _("Supplier")
        verbose_name_plural = _("Suppliers")

    def __str__(self):
        return self.name


class Restock(models.Model):
    STATUS_CHOICES = [
        ('PENDING', _('Pending')),
        ('ORDERED', _('Ordered')),
        ('RECEIVED', _('Received')),
        ('CANCELLED', _('Cancelled')),
    ]

    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, related_name="restocks",
                                 verbose_name=_("Supplier"))
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="restocks", verbose_name=_("Product"))
    quantity = models.PositiveIntegerField(_("Quantity"))
    status = models.CharField(_("Status"), max_length=20, choices=STATUS_CHOICES, default='PENDING')
    expected_date = models.DateField(_("Expected Date"), blank=True, null=True)
    notes = models.TextField(_("Notes"), blank=True, null=True)
    created_at = models.DateTimeField(_("Created At"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated At"), auto_now=True)

    class Meta:
        verbose_name = _("Restock")
        verbose_name_plural = _("Restocks")
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.product.name} - {self.quantity} units from {self.supplier.name}"