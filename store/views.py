from django.views.generic import ListView, DetailView, TemplateView
from django.views import View
from django.shortcuts import render, redirect
from .forms import PurchaseForm, UserRegisterForm
from .models import ProductCategory, Product, Purchase, PurchaseProduct
from django.db.models import Sum
from django.utils.dateparse import parse_date
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.auth import login
from django.utils import timezone
from django.utils.dateparse import parse_datetime


class CategoryListView(ListView):
    model = ProductCategory
    template_name = 'store/category_list.html'


class ProductListView(ListView):
    model = Product
    template_name = 'store/product_list.html'

    def get_queryset(self):
        return Product.objects.filter(category__title=self.kwargs['category'])


class ProductDetailView(DetailView):
    model = Product
    template_name = 'store/product_detail.html'


class ReportView(View):
    def get(self, request):
        products = Product.objects.all()
        return render(request, 'store/report.html', {'products': products})

    def post(self, request):
        selected_product_id = request.POST.get('product')
        start_date_str = request.POST.get('start_date') + " 00:00:00"
        end_date_str = request.POST.get('end_date') + " 23:59:59"

        # Convert to timezone-aware datetime objects
        start_date = timezone.make_aware(parse_datetime(start_date_str))
        end_date = timezone.make_aware(parse_datetime(end_date_str))

        purchases = PurchaseProduct.objects.filter(
            product_id=selected_product_id,
            purchase__purchase_date__range=[start_date, end_date],
        )
        total_revenue = sum(
            purchase.product.price * purchase.quantity for purchase in purchases
        )
        product = Product.objects.get(id=selected_product_id)

        return render(
            request,
            'store/report.html',
            {
                'total_revenue': total_revenue,
                'product': product,
                'purchases': purchases,
                'products': Product.objects.all(),
            },
        )


class PurchaseView(LoginRequiredMixin, View):
    def get(self, request):
        form = PurchaseForm()
        return render(request, 'store/purchase.html', {'form': form})

    def post(self, request):
        form = PurchaseForm(request.POST)
        if form.is_valid():
            purchase = Purchase.objects.create(
                user=request.user, purchase_date=timezone.now()
            )
            PurchaseProduct.objects.create(
                purchase=purchase,
                product=form.cleaned_data['product'],
                quantity=form.cleaned_data['quantity'],
            )
            return redirect('store:purchase_success')
        else:
            # If form is not valid, re-render the page with form errors
            return render(request, 'store/purchase.html', {'form': form})


class PurchaseSuccessView(TemplateView):
    template_name = 'store/purchase_success.html'


class HomeView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'store/home.html')


def register(request):
    """Function-based view for User registration"""
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            login(request, user)  # Log the user in after registering
            return redirect('store:home')
    else:
        form = UserRegisterForm()

    return render(request, 'store/register.html', {'form': form})
