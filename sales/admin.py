from django.contrib import admin
from .models import Sale, Product, Category


admin.site.register(Category)
admin.site.register(Product)


@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    def get_readonly_fields(self, request, obj = ...):
        if obj:
            if obj.payment_status == "P":
                return ["customer", "product", "bought_quantity", "payment_form", "price_on_sale"]
            return ["customer", "product", "bought_quantity", "payment_form", "price_on_sale", "payment_status"]
        
        return super().get_readonly_fields(request, obj)
    
    def save_model(self, request, obj, form, change):
        if not change:
            return super().save_model(request, obj, form, change)
        
        old_sale = Sale.objects.filter(id=obj.id).first()
            
        if old_sale is None:
            return super().save_model(request, obj, form, change)

        if old_sale.payment_status == "C":
            obj.payment_status = "C"
            return super().save_model(request, obj, form, change)
            
        if old_sale.payment_status == "P" and obj.payment_status == "C":
            obj.product.current_quantity -= obj.bought_quantity
            obj.product.save()

        return super().save_model(request, obj, form, change)
