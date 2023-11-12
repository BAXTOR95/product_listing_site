import os
import requests
from typing import Any
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from store.models import ProductCategory, Product


class Command(BaseCommand):
    help = 'Populates the database with products and categories from the Fake Store API'

    def handle(self, *args: Any, **kwargs: Any) -> str | None:
        # Fetch categories
        categories_response = requests.get(
            'https://fakestoreapi.com/products/categories'
        )
        categories = categories_response.json()

        for category_name in categories:
            ProductCategory.objects.get_or_create(title=category_name)

        # Fetch products
        products_response = requests.get('https://fakestoreapi.com/products')
        products = products_response.json()

        for product_data in products:
            category = ProductCategory.objects.get(title=product_data['category'])
            product = Product(
                category=category,
                title=product_data['title'],
                price=product_data['price'],
                description=product_data['description'],
                average_rating=product_data['rating']['rate'],
                rating_count=product_data['rating']['count'],
                # Image will be handle separately
            )

            # Handle image downloading
            image_url = product_data['image']
            response = requests.get(image_url)
            if response.status_code == 200:
                # Use the URL's filename as the image name
                image_name = os.path.basename(image_url)
                product.image.save(
                    image_name, ContentFile(response.content), save=False
                )

            product.save()

        self.stdout.write(self.style.SUCCESS('Successfully populated the database'))
