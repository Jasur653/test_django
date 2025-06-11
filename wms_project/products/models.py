from django.db import models
from django.utils.translation import gettext_lazy as _


class Category(models.Model):
    name = models.CharField(_("Category Name"), max_length=100)
    description = models.TextField(_("Description"), blank=True, null=True)
    created_at = models.DateTimeField(_("Created At"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated At"), auto_now=True)

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")

    def __str__(self):
        return self.name


class Product(models.Model):
    SIZE_CHOICES = [
        ('XS', 'Extra Small'),
        ('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large'),
        ('XL', 'Extra Large'),
        ('XXL', 'Double Extra Large'),
    ]

    name = models.CharField(_("Product Name"), max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="products",
                                 verbose_name=_("Category"))
    description = models.TextField(_("Description"), blank=True, null=True)
    quantity = models.PositiveIntegerField(_("Quantity"), default=0)
    size = models.CharField(_("Size"), max_length=3, choices=SIZE_CHOICES)
    color = models.CharField(_("Color"), max_length=50)
    price = models.DecimalField(_("Price"), max_digits=10, decimal_places=2)
    image = models.ImageField(_("Image"), upload_to='products/', blank=True, null=True)
    low_stock_threshold = models.PositiveIntegerField(_("Low Stock Threshold"), default=10)
    created_at = models.DateTimeField(_("Created At"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated At"), auto_now=True)

    class Meta:
        verbose_name = _("Product")
        verbose_name_plural = _("Products")

    def __str__(self):
        return self.name

    @property
    def is_low_stock(self):
        return self.quantity <= self.low_stock_threshold