from django.contrib import admin
from .models import Sale, Product, Category


admin.site.register(Category)
admin.site.register(Product)


@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    readonly_fields = ["customer", "product", "bought_quantity", "payment_form", "price_on_sale"]
