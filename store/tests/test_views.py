import os
from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from django.core.files.uploadedfile import SimpleUploadedFile
from ..models import ProductCategory, Product, Purchase, PurchaseProduct

# Tests for HomeView


class HomeViewTest(TestCase):
    """
    Test suite for the HomeView.
    """

    def test_view_url_exists_at_desired_location(self):
        """
        Ensure that the HomeView is accessible at the correct URL.
        """
        response = self.client.get('/store/')
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        """
        Verify that the HomeView uses the appropriate template.
        """
        response = self.client.get(reverse('store:home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'store/home.html')


# Tests for CategoryListView


class CategoryListViewTest(TestCase):
    """
    Test suite for the CategoryListView.
    """

    def test_view_url_exists_at_desired_location(self):
        """
        Ensure that the CategoryListView is accessible at the correct URL.
        """
        response = self.client.get('/store/categories/')
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        """
        Verify that the CategoryListView uses the appropriate template.
        """
        response = self.client.get(reverse('store:category_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'store/category_list.html')


# Tests for ProductListView


class ProductListViewTest(TestCase):
    """
    Test suite for the ProductListView.
    """

    @classmethod
    def setUpTestData(cls):
        """
        Set up data for the entire test suite.
        """
        ProductCategory.objects.create(title='Electronics')

    def test_view_url_exists_at_desired_location(self):
        """
        Ensure that the ProductListView is accessible at the correct URL.
        """
        response = self.client.get('/store/categories/Electronics/')
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        """
        Verify that the ProductListView uses the appropriate template.
        """
        response = self.client.get(
            reverse('store:product_list', kwargs={'category': 'Electronics'})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'store/product_list.html')


# Tests for ProductDetailView


class ProductDetailViewTest(TestCase):
    """
    Test suite for the ProductDetailView.
    """

    @classmethod
    def setUpTestData(cls):
        """
        Set up data for the entire test suite.
        """
        category = ProductCategory.objects.create(title='Electronics')
        # Create a dummy image file
        image_path = os.path.join(os.path.dirname(__file__), 'dummy_image.jpg')
        image = SimpleUploadedFile(
            name='test_image.jpg',
            content=open(image_path, 'rb').read(),
            content_type='image/jpeg',
        )
        Product.objects.create(
            category=category,
            title='Laptop',
            price=1000.00,
            average_rating=4.5,
            rating_count=10,
            image=image,
        )

    def test_view_url_exists_at_desired_location(self):
        """
        Ensure that the ProductDetailView is accessible at the correct URL.
        """
        response = self.client.get('/store/products/1/')
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        """
        Verify that the ProductDetailView uses the appropriate template.
        """
        response = self.client.get(reverse('store:product_detail', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'store/product_detail.html')


# Tests for ReportView


class ReportViewTest(TestCase):
    """
    Test suite for the ReportView.
    """

    @classmethod
    def setUpTestData(cls):
        """
        Set up data for the entire test suite.
        """
        # Create test data
        category = ProductCategory.objects.create(title='Electronics')
        product = Product.objects.create(
            category=category,
            title='Laptop',
            price=1000.00,
            average_rating=4.5,
            rating_count=10,
        )
        user = User.objects.create_user('testuser', 'test@example.com', 'password')
        purchase_date = timezone.now()
        purchase = Purchase.objects.create(user=user, purchase_date=purchase_date)
        PurchaseProduct.objects.create(purchase=purchase, product=product, quantity=2)

        # Create a staff user
        cls.staff_user = User.objects.create_user(
            'staffuser', 'staff@example.com', 'password', is_staff=True
        )

        # Create a non-staff user
        cls.non_staff_user = User.objects.create_user(
            'nonstaffuser', 'nonstaff@example.com', 'password', is_staff=False
        )

    def test_staff_user_access(self):
        """
        Test that a staff user can access the ReportView.
        """
        self.client.login(username='staffuser', password='password')
        response = self.client.get(reverse('store:report_view'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'store/report.html')

    def test_non_staff_user_access(self):
        """
        Test that a non-staff user is redirected or denied access.
        """
        self.client.login(username='nonstaffuser', password='password')
        response = self.client.get(reverse('store:report_view'))
        self.assertNotEqual(response.status_code, 200)

    def test_anonymous_user_access(self):
        """
        Test that an anonymous user is redirected to the login page.
        """
        response = self.client.get(reverse('store:report_view'))
        self.assertNotEqual(response.status_code, 200)

    def test_get_request(self):
        """
        Ensure that the ReportView returns the correct template and status code on GET request.
        """
        # Log in as a staff user
        self.client.login(username='staffuser', password='password')

        # Simulate GET request
        response = self.client.get(reverse('store:report_view'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'store/report.html')

    def test_post_request(self):
        """
        Test the functionality of ReportView on POST request with valid data.
        """
        # Log in as a staff user
        self.client.login(username='staffuser', password='password')

        # Simulate POST request with data
        start_date = timezone.now() - timezone.timedelta(days=1)
        end_date = timezone.now() + timezone.timedelta(days=1)
        post_data = {
            'product': 1,  # Assuming the product ID is 1
            'start_date': start_date.strftime('%Y-%m-%d'),
            'end_date': end_date.strftime('%Y-%m-%d'),
        }
        response = self.client.post(reverse('store:report_view'), post_data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'store/report.html')

        # Check if the context data contains the expected keys
        self.assertIn('total_revenue', response.context)
        self.assertIn('product', response.context)
        self.assertIn('purchases', response.context)


# Testing Purchase View


class PurchaseViewTest(TestCase):
    """
    Test suite for the PurchaseView.
    """

    def setUp(self):
        """
        Set up a user for testing the PurchaseView.
        """
        # Create a user for login
        self.user = User.objects.create_user(username='testuser', password='password')
        self.client = Client()

    def test_get_request(self):
        """
        Ensure that the PurchaseView returns the correct template and status code on GET request.
        """
        # Log in the user
        self.client.login(username='testuser', password='password')

        # Get the response
        response = self.client.get(reverse('store:purchase_view'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'store/purchase.html')

    def test_post_request(self):
        """
        Test the functionality of PurchaseView on POST request with valid data.
        """
        # Log in the user
        self.client.login(username='testuser', password='password')

        # Create necessary data for the POST request
        category = ProductCategory.objects.create(title='Electronics')
        product = Product.objects.create(
            category=category,
            title='Laptop',
            price=1000.00,
            average_rating=4.5,
            rating_count=10,
        )

        # Simulate POST request with valid form data
        post_data = {'product': product.id, 'quantity': 1}
        response = self.client.post(reverse('store:purchase_view'), post_data)

        # Check if the response is a redirect to the purchase success page
        self.assertRedirects(response, reverse('store:purchase_success'))

        # Optionally, check if the Purchase and PurchaseProduct objects are created
        self.assertTrue(Purchase.objects.exists())
        self.assertTrue(PurchaseProduct.objects.exists())


# Testing PurchaseSuccessView


class PurchaseSuccessViewTest(TestCase):
    """
    Test suite for the PurchaseSuccessView.
    """

    def test_view_url_exists_at_desired_location(self):
        """
        Ensure that the PurchaseSuccessView is accessible at the correct URL.
        """
        response = self.client.get('/store/purchase/success/')
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        """
        Verify that the PurchaseSuccessView uses the appropriate template.
        """
        response = self.client.get(reverse('store:purchase_success'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'store/purchase_success.html')


# Testing RegisterView


class RegisterViewTest(TestCase):
    """
    Test suite for the register view.
    """

    def test_get_request(self):
        """
        Ensure that the register view returns the correct template and status code on a GET request.
        """
        response = self.client.get(reverse('store:register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'store/register.html')

    def test_post_request_with_valid_data(self):
        """
        Test the functionality of the register view on a POST request with valid data.
        """
        post_data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
        }
        response = self.client.post(reverse('store:register'), post_data)
        self.assertEqual(
            response.status_code, 302
        )  # Redirect after successful registration
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_post_request_with_invalid_data(self):
        """
        Test the register view with invalid POST data to ensure it doesn't create a user.
        """
        post_data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'testpassword123',
            'password2': 'wrongconfirmation',
        }
        response = self.client.post(reverse('store:register'), post_data)
        self.assertEqual(
            response.status_code, 200
        )  # Stays on the same page due to form errors
        self.assertFalse(User.objects.filter(username='newuser').exists())
