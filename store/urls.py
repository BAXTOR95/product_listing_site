from django.urls import path
from .views import (
    CategoryListView,
    ProductListView,
    ProductDetailView,
    ReportView,
    PurchaseView,
    PurchaseSuccessView,
    HomeView,
    register,
)
from django.contrib.auth.views import LoginView, LogoutView

app_name = 'store'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('register/', register, name='register'),
    path('login/', LoginView.as_view(template_name='store/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('categories/', CategoryListView.as_view(), name='category_list'),
    path('categories/<str:category>/', ProductListView.as_view(), name='product_list'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('report/', ReportView.as_view(), name='report_view'),
    path('purchase/', PurchaseView.as_view(), name='purchase_view'),
    path('purchase/success/', PurchaseSuccessView.as_view(), name='purchase_success'),
]
