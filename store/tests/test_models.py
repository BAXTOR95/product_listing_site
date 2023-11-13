from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone
from decimal import Decimal
from ..models import ProductCategory, Product, Purchase, PurchaseProduct

# Testing Product Category model


class ProductCategoryModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create test data for all test methods in this class
        ProductCategory.objects.create(title='Electronics')

    def test_title_label(self):
        """Checks if the title field of the ProductCategory model contains the correct data"""
        category = ProductCategory.objects.get(id=1)
        field_label = category._meta.get_field('title').verbose_name
        self.assertEqual(field_label, 'title')

    def test_title_max_length(self):
        """Checks if the max_length set in the title field of the ProductCategory model is 200"""
        category = ProductCategory.objects.get(id=1)
        max_length = category._meta.get_field('title').max_length
        self.assertEqual(max_length, 200)

    def test_object_name_is_title(self):
        """Checks if the string representation of the ProductCategory objects is the title"""
        category = ProductCategory.objects.get(id=1)
        expected_object_name = category.title
        self.assertEqual(expected_object_name, str(category))


# Testing Product model


class ProductModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create test data for all test methods in this class
        category = ProductCategory.objects.create(title='Books')
        Product.objects.create(
            category=category,
            title='Django for Beginners',
            price=29.99,
            description='Learn Django',
            average_rating=4.5,
            rating_count=10,
        )

    def test_title_content(self):
        """Checks if the title field of the Product model contains the correct data"""
        product = Product.objects.get(id=1)
        expected_title = 'Django for Beginners'
        self.assertEqual(product.title, expected_title)

    def test_price_content(self):
        """Verifies the price field"""
        product = Product.objects.get(id=1)
        expected_price = Decimal('29.99')
        self.assertEqual(product.price, expected_price)

    def test_description_content(self):
        """Ensures the description field is correctly populated"""
        product = Product.objects.get(id=1)
        expected_description = 'Learn Django'
        self.assertEqual(product.description, expected_description)

    def test_average_rating_content(self):
        """Validates the average_rating field"""
        product = Product.objects.get(id=1)
        expected_average_rating = 4.5
        self.assertEqual(product.average_rating, expected_average_rating)

    def test_rating_count_content(self):
        """Validates the rating_count field"""
        product = Product.objects.get(id=1)
        expected_rating_count = 10
        self.assertEqual(product.rating_count, expected_rating_count)

    def test_category_relationship(self):
        """tests the ForeignKey relationship between Product and ProductCategory."""
        product = Product.objects.get(id=1)
        self.assertEqual(product.category.title, 'Books')


# Testing Purchase and Purchase Product Models


class PurchaseProductModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create test data for all test methods in this class
        user = User.objects.create(username='testuser', password='12345')
        category = ProductCategory.objects.create(title='Electronics')
        product = Product.objects.create(
            category=category,
            title='Laptop',
            price=1000.00,
            average_rating=4.5,
            rating_count=10,
        )
        purchase_date = timezone.now()
        purchase = Purchase.objects.create(user=user, purchase_date=purchase_date)
        PurchaseProduct.objects.create(purchase=purchase, product=product, quantity=2)

    def test_purchase_date(self):
        """Test that the purchase_date field is set correctly"""
        purchase = Purchase.objects.get(id=1)
        self.assertIsNotNone(purchase.purchase_date)

    def test_purchase_relationship(self):
        """Test the relationship between PurchaseProduct and Purchase models"""
        purchase_product = PurchaseProduct.objects.get(id=1)
        self.assertEqual(purchase_product.purchase.user.username, 'testuser')

    def test_product_relationship(self):
        """Test the relationship between PurchaseProduct and Product models"""
        purchase_product = PurchaseProduct.objects.get(id=1)
        self.assertEqual(purchase_product.product.title, 'Laptop')

    def test_quantity_content(self):
        """Test that the quantity field in PurchaseProduct model stores data correctly"""
        purchase_product = PurchaseProduct.objects.get(id=1)
        expected_quantity = 2
        self.assertEqual(purchase_product.quantity, expected_quantity)

    # Add more tests for fields like quantity
