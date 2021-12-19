from django.contrib import admin

from .models import OrderProduct, Order

@admin.register(OrderProduct)
class OrderProductAdmin(admin.ModelAdmin):
    list_display = ("id", "product", "quantity", "price","discount","sub_total")
    

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("bill_number", "customer", "store", "order_status","total")
    list_filter = ("customer", "store", "order_status", "total")
    search_fields = ("bill_number", "customer__first_name")

