# from django.db import models
# from common.models import TimeStampedModel
# class Product(models.Model):
#     name = models.CharField(max_length=255, unique=True)
#     quantity = models.IntegerField(blank=True, default=0)
#     description = models.TextField(blank=True)
    
#     def __str__(self):
#         return self.name


# class Attribute(models.Model):
#     name = models.CharField(max_length=25)

#     def __str__(self):
#         return self.name


# class AttributeValue(models.Model):
#     attribute = models.ForeignKey(Attribute, related_name='attribute_value', on_delete=models.CASCADE)
#     value = models.CharField(max_length=25)

#     def __str__(self):
#         return "{0}-{1}".format(self.attribute, self.value)


# class ProductVarient(models.Model):
#     varient_name = models.CharField(max_length=100, )
#     product = models.ForeignKey(Product, related_name='product_varient', on_delete=models.CASCADE)
#     old_price = models.FloatField()
#     price = models.FloatField(blank=True, null=True)
#     cost_price = models.FloatField(blank=True, null=True)
#     quantity = models.IntegerField()
#     attribut_value = models.ManyToManyField(AttributeValue, related_name='attribute_product_varient', blank=True)

#     def __str__(self):
#         return self.varient_name


# class Price(TimeStampedModel):
#     product= models.ForeignKey(Product, on_delete=models.CASCADE, related_name="price")
#     price = models.PositiveIntegerField(default=0)

#     def __str__(self):
#         return f"{self.product.name}"


import random
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import Sum
from django.utils.text import slugify

from common.models import Identifier,TimeStampedModel
from .managers import SubCategoryManager
from .managers import ProductManager
from store.models import Company,Store



class ProductCategory(Identifier):
    is_active = models.BooleanField(default=True)
    image = models.URLField(blank=True)
    description = models.TextField(default="-",max_length=500)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="category")

    class Meta:
        verbose_name = "Product Category"
        verbose_name_plural = "Product Categories"


class ProductSubCategory(Identifier):
    category = models.ForeignKey(ProductCategory, on_delete=models.PROTECT, related_name="sub_categories")
    is_active = models.BooleanField(default=True)
    image = models.URLField(blank=True)
    description = models.TextField(default="-",max_length=500)

    objects = SubCategoryManager()

    class Meta:
        verbose_name = "Product SubCategory"
        verbose_name_plural = "Product Sub-Categories"


class Product(Identifier,TimeStampedModel):
    sku = models.CharField(primary_key=True, max_length=200,blank=True,unique=True)
    sub_category = models.ForeignKey(ProductSubCategory, on_delete=models.PROTECT,related_name="products")
    description = models.TextField(blank=True,max_length=500)
    active = models.BooleanField(default=True, blank=True)
    image = models.URLField(blank=True)
    objects = ProductManager()

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):

        if not self.sku:
            sku=''
            
            company_name = self.sub_category.category.company.name.split()
            company_sku = ''
            if len(company_name)>1:
                for item in company_name:
                    company_sku=company_sku+item[0][0].lower()
            else:
                company_sku=company_name[0][0:3].lower()

            sub_category_name = self.sub_category.name.split()
            sub_category_sku=''
            if len(sub_category_name) > 1:
                for item in sub_category_name:
                    sub_category_sku = sub_category_sku+item[0][0].lower()
            else:
                sub_category_sku = (sub_category_name[0][0:3].lower())

            product_name = self.name.split()
            product_sku=''
            if len(product_name) > 1:
                for item in product_name:
                    product_sku = product_sku+item[0][0].lower()
            else:
                product_sku = (product_name[0][0:3].lower())

            sku = company_sku + '-' + sub_category_sku + '-' + product_sku + '-' + str(random.randint(0, 1000))
            self.sku = sku


        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

class Price(TimeStampedModel):
    sku= models.ForeignKey(Product, on_delete=models.CASCADE, related_name="price")
    price = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.product.name}"
        
class ConsolidatedStoreProduct(models.Model):
    class Meta:
        unique_together = (('store', 'sku'),)
    store= models.ForeignKey(Store, on_delete=models.CASCADE, related_name="consolidated_store_product")
    sku = models.ForeignKey(Product,on_delete=models.CASCADE,related_name="consolidated_store_products")

    def __str__(self):
        return f"{self.store.name}-{self.product.name}"


