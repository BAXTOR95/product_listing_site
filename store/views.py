from django.views.generic import ListView, DetailView
from django.views import View
from django.shortcuts import render
from .models import ProductCategory, Product, Purchase
from django.db.models import Sum
from django.utils.dateparse import parse_date


class CategoryListView(ListView):
    model = ProductCategory
    template_name = 'store/category_list.html'


class ProductListView(ListView):
    model = Product
    template_name = 'store/product_list.html'

    def get_queryset(self):
        return Product.objects.filter(category__tile=self.kwargs['category'])


class ProductDetailView(DetailView):
    model = Product
    template_name = 'store/product_detail.html'


class ReportView(View):
    def get(self, request):
        products = Product.objects.all()
        return render(request, 'store/report.html', {'products': products})

    def post(self, request):
        selected_product_id = request.POST.get('product')
        start_date = parse_date(request.POST.get('start_date'))
        end_date = parse_date(request.POST.get('end_date'))

        purchases = Purchase.objects.filter(
            product_id=selected_product_id, purchase_date__range=[start_date, end_date]
        )

        total_revenue = (
            purchases.aggregate(Sum('product__price'))['product__price__sum'] or 0
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
