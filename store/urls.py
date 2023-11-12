from django.urls import path
from .views import CategoryListView, ProductListView, ProductDetailView, ReportView

app_name = 'store'

urlpatterns = [
    path('categories/', CategoryListView.as_view(), name='category_list'),
    path('categories/<str:category>/', ProductListView.as_view(), name='product_list'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('report/', ReportView.as_view(), name='report_view'),
]
