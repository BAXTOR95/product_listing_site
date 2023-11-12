from django.views.generic import ListView, DetailView
from .models import ProductCategory, Product


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
