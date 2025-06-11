from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Product, Category

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input'}),
            'description': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 3}),
        }

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'category', 'description', 'quantity', 'size', 'color', 'price', 'image', 'low_stock_threshold']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'description': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 3}),
            'quantity': forms.NumberInput(attrs={'class': 'form-input'}),
            'size': forms.Select(attrs={'class': 'form-select'}),
            'color': forms.TextInput(attrs={'class': 'form-input'}),
            'price': forms.NumberInput(attrs={'class': 'form-input', 'step': '0.01'}),
            'low_stock_threshold': forms.NumberInput(attrs={'class': 'form-input'}),
        }