from django.contrib import admin

from .models import (
    Product,
    Attribute,
    AttributeValue,
    ProductVarient
)

class ProductVarientInline(admin.StackedInline):
    model = ProductVarient

@admin.register(Product)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'quantity']
    list_filter = ['name',]
    search_fields = ['name',]
    inlines = [ProductVarientInline]

admin.site.register(Attribute)
admin.site.register(AttributeValue)