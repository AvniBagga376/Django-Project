from django.db import models
from datetime import date

# Create your models here.
class Contact(models.Model):
    name= models.CharField(max_length=122)
    phone= models.CharField(max_length=12)
    email = models.CharField(max_length=122)
    desc = models.TextField(max_length=200)
    date = models.DateField(default=date.today)

    def __str__(self):
        return self.name
    
class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    product_id = models.CharField(max_length=50, unique=True, default='xxx')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField(default=0)

    def __str__(self):
        return self.name
    
class StockHistory(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    stock_in = models.IntegerField(default=0)
    stock_out = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.product.name} - {self.date}"
    
