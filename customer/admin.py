from django.contrib import admin

from .models import (
    CustomerTier,
    Customer,
)


@admin.register(CustomerTier)
class CustomerTierAdmin(admin.ModelAdmin):
    list_display = ("id","name","discount")
    list_filter = ("discount",)

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ("customer_id",)
    # list_filter = ("phone_number", "is_active")