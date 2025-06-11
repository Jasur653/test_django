from django import forms
from django.utils.translation import gettext_lazy as _
from .models import StockMovement

class StockMovementForm(forms.ModelForm):
    class Meta:
        model = StockMovement
        fields = ['product', 'movement_type', 'quantity', 'reason']
        widgets = {
            'product': forms.Select(attrs={'class': 'form-select'}),
            'movement_type': forms.Select(attrs={'class': 'form-select'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-input', 'min': 1}),
            'reason': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 3}),
        }