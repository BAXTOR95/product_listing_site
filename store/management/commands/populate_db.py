import os
import requests
import pytz
from datetime import datetime
from typing import Any
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from store.models import ProductCategory, Product, Purchase, PurchaseProduct
from django.contrib.auth.models import User
from django.utils import timezone


class Command(BaseCommand):
    help = 'Populates the database with products and categories from the Fake Store API'

    def handle(self, *args: Any, **kwargs: Any) -> str | None:
        # Fetch user details
        users_response = requests.get('https://fakestoreapi.com/users')
        users_data = users_response.json()
        users_dict = {user['id']: user for user in users_data}

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

        # Fetch cart data
        carts_response = requests.get('https://fakestoreapi.com/carts')
        carts = carts_response.json()

        for cart in carts:
            user_data = users_dict.get(cart['userId'])
            if user_data:
                user, created = User.objects.get_or_create(
                    username=user_data['username'],
                    defaults={
                        'email': user_data['email'],
                        'first_name': user_data['name']['firstname'],
                        'last_name': user_data['name']['lastname'],
                    },
                )
                if created:
                    user.set_password(user_data['password'])
                    user.save()

                # Parse the purchase date from the API
                naive_purchase_date = datetime.strptime(
                    cart['date'], '%Y-%m-%dT%H:%M:%S.%fZ'
                )
                new_york_tz = pytz.timezone('America/New_York')
                purchase_date = timezone.make_aware(naive_purchase_date, new_york_tz)

                purchase = Purchase.objects.create(
                    user=user, purchase_date=purchase_date
                )

                for item in cart['products']:
                    product = Product.objects.get(id=item['productId'])
                    PurchaseProduct.objects.create(
                        purchase=purchase, product=product, quantity=item['quantity']
                    )

        self.stdout.write(self.style.SUCCESS('Successfully populated the database'))
