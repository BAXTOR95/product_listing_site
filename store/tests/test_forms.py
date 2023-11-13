from django.test import TestCase
from store.forms import PurchaseForm, UserRegisterForm
from store.models import Product, ProductCategory
from django.contrib.auth.models import User


# Tests for PurchaseForm


class PurchaseFormTest(TestCase):
    """
    Test suite for the PurchaseForm.
    """

    @classmethod
    def setUpTestData(cls):
        category = ProductCategory.objects.create(title='Electronics')
        cls.product = Product.objects.create(
            category=category,
            title='Laptop',
            price=1000.00,
            average_rating=4.5,
            rating_count=10,
        )

    def test_purchase_form_valid_data(self):
        """
        Test the PurchaseForm with valid data.
        """
        form = PurchaseForm(data={'product': self.product.id, 'quantity': 2})
        self.assertTrue(form.is_valid())

    def test_purchase_form_quantity_initial_value(self):
        """
        Test that the initial value of quantity is set correctly.
        """
        form = PurchaseForm()
        self.assertEqual(form.fields['quantity'].initial, 1)

    def test_purchase_form_quantity_min_value(self):
        """
        Test that the minimum value of quantity is enforced.
        """
        form = PurchaseForm(data={'product': self.product.id, 'quantity': 0})
        self.assertFalse(form.is_valid())
        self.assertIn('quantity', form.errors)
        self.assertEqual(form.errors['quantity'], ['Quantity must be at least 1.'])


# Tests for UserRegisterForm


class UserRegisterFormTest(TestCase):
    """
    Test suite for the UserRegisterForm.
    """

    def test_user_register_form_valid_data(self):
        """
        Test the UserRegisterForm with valid data.
        """
        form = UserRegisterForm(
            data={
                'username': 'newuser',
                'email': 'newuser@example.com',
                'password1': 'testpassword123',
                'password2': 'testpassword123',
            }
        )
        self.assertTrue(form.is_valid())

    def test_user_register_form_email_field(self):
        """
        Test that the email field is required and validated.
        """
        form = UserRegisterForm(
            data={
                'username': 'newuser',
                'email': '',  # Empty email
                'password1': 'testpassword123',
                'password2': 'testpassword123',
            }
        )
        self.assertFalse(form.is_valid())

    def test_user_register_form_saves_user(self):
        """
        Test if the UserRegisterForm saves a user correctly with valid data.
        """
        form = UserRegisterForm(
            data={
                'username': 'newuser',
                'email': 'newuser@example.com',
                'password1': 'testpassword123',
                'password2': 'testpassword123',
            }
        )
        if form.is_valid():
            form.save()
        self.assertTrue(User.objects.filter(username='newuser').exists())
