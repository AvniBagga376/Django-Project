from django import forms
from .models import Category, Product, StockHistory

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Category Name'}),
        }

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'category', 'product_id', 'price']

from django import forms
from .models import StockHistory

class StockHistoryForm(forms.ModelForm):
    class Meta:
        model = StockHistory
        fields = ['stock_in']  # Only include stock_in for adding quantities
