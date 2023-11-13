from django.contrib import admin
from .models import Product, ProductCategory, Purchase, PurchaseProduct

admin.site.site_title = 'Online Store admin'
admin.site.site_header = 'Online Store administration'
admin.site.index_title = 'Online Store administration'
admin.site.register(Product)
admin.site.register(ProductCategory)
admin.site.register(Purchase)
admin.site.register(PurchaseProduct)
