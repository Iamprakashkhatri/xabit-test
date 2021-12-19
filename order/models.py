import random
import os
import uuid
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import Avg

from common.models import TimeStampedModel
from product.models import Product
from customer.models import Customer
from store.models import Store
import datetime as dt


class Order(TimeStampedModel):
    ORDER_STATUS = (('Created', 'Created'),
                    ('In Progress', 'In Progress'), 
                    ('Completed', 'Completed'),
                    ('Cancelled', 'Cancelled'))

    ORDER_TYPE = (('Dine-in','Dine-in'),
    				('Take-away','Take-away'))

    bill_number = models.CharField(max_length=200, primary_key=True, blank=True, unique=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE,related_name='order')
    store = models.ForeignKey(Store,on_delete=models.CASCADE, related_name='orders')
    order_status = models.CharField(max_length=100, choices=ORDER_STATUS, default="Created")
    processed_by = models.CharField(max_length=255, default="", blank=True)
    order_type = models.CharField(max_length=100, choices=ORDER_TYPE, default="Ordered")
    total = models.PositiveIntegerField()
    taxable_amount = models.PositiveIntegerField(default=0)
    tax_amount = models.PositiveIntegerField(null=True, blank=True)
    bill_amount = models.PositiveIntegerField(null=True, blank=True)
    vat_refund_amount = models.PositiveIntegerField(null=True, blank=True)
    table_no = models.CharField(max_length=100,null=True,blank=True)

    def __str__(self):
        return  str(self.customer.user.first_name)+ '-' + self.store.name

    def save(self, *args, **kwargs):
        if not self.bill_number:
            bill_number=''
            
            company_name = self.store.company.name.split()
            company_bill_number = ''
            if len(company_name)>1:
                for item in company_name:
                    company_bill_number=company_bill_number+item[0][0].lower()
            else:
                company_bill_number=company_name[0][0:3].lower()
            store_name = self.store.name.split()
            store_bill_number=''
            if len(store_name) > 1:
                for item in store_name:
                    store_bill_number = store_bill_number+item[0][0].lower()
            else:
                store_bill_number = (store_name[0][0:3].lower())
            last_invoice = Order.objects.all().order_by('created_at').last()
            client_initials = self.store.company.company_bills_code + '-'
            if not last_invoice:
                new_invoice_no = client_initials + '1'
            else:
                invoice_no = last_invoice.bill_number
                invoice_int = int(invoice_no.split('-')[-1])
                new_invoice_int = invoice_int + 1
                new_invoice_no = client_initials + str(new_invoice_int)

            bill_number = company_bill_number + '-' + store_bill_number + '-' + str(dt.datetime.now().year)[-2:]+'-' + \
                            new_invoice_no

            self.bill_number = bill_number

        super().save(*args, **kwargs)

class OrderProduct(TimeStampedModel):
    order = models.ForeignKey(Order,on_delete=models.CASCADE,related_name='order_products')
    product = models.ForeignKey(Product, on_delete=models.CASCADE,related_name='order_product')
    quantity = models.PositiveIntegerField(default=1)
    price = models.PositiveIntegerField()
    discount = models.DecimalField(max_digits=4, decimal_places=2, blank=True, default=0)
    sub_total = models.PositiveIntegerField()
    reedem = models.BooleanField()
    
    def __str__(self):
        return f'{self.quantity} of {self.product.name}'


