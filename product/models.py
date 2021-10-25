from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=255, unique=True)
    quantity = models.IntegerField(blank=True, default=0)
    description = models.TextField(blank=True)
    
    def __str__(self):
        return self.name


class Attribute(models.Model):
    name = models.CharField(max_length=25)

    def __str__(self):
        return self.name


class AttributeValue(models.Model):
    attribute = models.ForeignKey(Attribute, related_name='attribute_value', on_delete=models.CASCADE)
    value = models.CharField(max_length=25)

    def __str__(self):
        return "{0}-{1}".format(self.attribute, self.value)


class ProductVarient(models.Model):
    varient_name = models.CharField(max_length=100, )
    product = models.ForeignKey(Product, related_name='product_varient', on_delete=models.CASCADE)
    old_price = models.FloatField()
    price = models.FloatField(blank=True, null=True)
    cost_price = models.FloatField(blank=True, null=True)
    quantity = models.IntegerField()
    attribut_value = models.ManyToManyField(AttributeValue, related_name='attribute_product_varient', blank=True)

    def __str__(self):
        return self.varient_name