from django.db import models
from django.contrib.auth.models import User


class ProductCategory(models.Model):
    title = models.CharField(max_length=200)

    def __str__(self) -> str:
        return self.title


class Product(models.Model):
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    image = models.ImageField(upload_to='product_images/')
    average_rating = models.FloatField()
    rating_count = models.IntegerField()

    def __str__(self) -> str:
        return self.title


class Purchase(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ManyToManyField(Product, through='PurchaseProduct')
    purchase_date = models.DateTimeField()

    def __str__(self) -> str:
        return f'{self.user.username} - {self.purchase_date}'


class PurchaseProduct(models.Model):
    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def __str__(self) -> str:
        return f'{self.purchase} - {self.product.title} x {self.quantity}'
