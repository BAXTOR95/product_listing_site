from django.urls import path
from .views import CategoryListView, ProductListView

app_name = 'store'

urlpatterns = [
    path('categories/', CategoryListView.as_view(), name='category_list'),
    path('categories/<str:category>/', ProductListView.as_view(), name='product_list'),
]
