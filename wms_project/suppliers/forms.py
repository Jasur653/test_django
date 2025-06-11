from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Supplier, Restock

class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = ['name', 'contact_person', 'email', 'phone', 'address', 'products']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input'}),
            'contact_person': forms.TextInput(attrs={'class': 'form-input'}),
            'email': forms.EmailInput(attrs={'class': 'form-input'}),
            'phone': forms.TextInput(attrs={'class': 'form-input'}),
            'address': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 3}),
            'products': forms.SelectMultiple(attrs={'class': 'form-multiselect'}),
        }

class RestockForm(forms.ModelForm):
    class Meta:
        model = Restock
        fields = ['supplier', 'product', 'quantity', 'status', 'expected_date', 'notes']
        widgets = {
            'supplier': forms.Select(attrs={'class': 'form-select'}),
            'product': forms.Select(attrs={'class': 'form-select'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-input', 'min': 1}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'expected_date': forms.DateInput(attrs={'class': 'form-input', 'type': 'date'}),
            'notes': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 3}),
        }