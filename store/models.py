from django.db import models


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
