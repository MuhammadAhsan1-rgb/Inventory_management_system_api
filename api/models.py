from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100 , unique=True)
    description = models.TextField(blank=True)

class Product(models.Model):
    product_name = models.CharField(max_length=100)
    category = models.ForeignKey(Category , on_delete=models.PROTECT , related_name="products")
    price =  models.DecimalField(max_digits=10 , decimal_places=2)
    stock =models.PositiveIntegerField()
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    