# from django.contrib import admin

# from .models import (
#     Product,
#     Attribute,
#     AttributeValue,
#     ProductVarient,
#     Price
# )

# class ProductVarientInline(admin.StackedInline):
#     model = ProductVarient

# @admin.register(Product)
# class CourseAdmin(admin.ModelAdmin):
#     list_display = ['id', 'name', 'quantity']
#     list_filter = ['name',]
#     search_fields = ['name',]
#     inlines = [ProductVarientInline]

# admin.site.register(Attribute)
# admin.site.register(AttributeValue)
# admin.site.register(Price)


from django.contrib import admin

from .models import (
    ProductCategory,
    ProductSubCategory,
    Product,
    Price,
    ConsolidatedStoreProduct,
)
admin.site.register(ProductCategory)
admin.site.register(ProductSubCategory)
admin.site.register(Product)
admin.site.register(Price)
admin.site.register(ConsolidatedStoreProduct)