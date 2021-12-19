from decimal import Decimal
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate

from django_filters.rest_framework import DjangoFilterBackend
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import Group

from rest_framework import status, viewsets
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
# from rest_framework_jwt.settings import api_settings

from .models import *
from .serializers import *


class OrderCreateAPI(APIView):
    """
    API View to POST order
    Required Data Format
        {
        "customer":1,
        "store":1,
        "total":10,
        "taxable_amount":900,
        "tax_amount":900,
        "bill_amount":150,
        "vat_refund_amount":1050,
        "table_no":"10a",
        "orderProducts": [
        {
        "sku": "hj-woe-esp-690",
        "quantity": 10,
        "price":4000,
        "discount":300,
        "sub_total":3000,
        "reedem":true
        },
        {
        "sku": "hj-woe-ep-670",
        "quantity": 5,
        "price":4000,
        "discount":300,
        "sub_total":3000,
        "reedem":true
        }
        ]
        }
    """
    permission_classes = (IsAuthenticated,)
    def post(self, request, *args, **kwargs):
        user = request.user
        customer = Customer.objects.get(user=user.pk)
        store_id = request.data['store']
        store = Store.objects.get(id=store_id)
        orderProducts = request.data['orderProducts']
        total = int(request.data['total'])
        taxable_amount = int(request.data['taxable_amount'])

        tax_amount = int(request.data['tax_amount'])
        bill_amount = int(request.data['bill_amount'])
        vat_refund_amount = int(request.data['vat_refund_amount'])
        table_no = request.data['table_no']

        if not orderProducts:
                return Response({'message': 'Cart is Empty'}, status=400)

        final_order = Order.objects.create(customer=customer,store=store, total=total, 
        								   taxable_amount=taxable_amount,tax_amount=tax_amount,
        								   bill_amount=bill_amount,vat_refund_amount=vat_refund_amount,
        								   table_no=table_no)
        final_order.save()
        for order_product in orderProducts:
            product = Product.objects.get(sku=order_product['sku'])
            quantity = order_product['quantity']
            price = int(order_product['price'])
            discount = Decimal(order_product['discount'])
            sub_total = int(order_product['sub_total'])
            reedem = order_product['reedem']
            order_product = OrderProduct.objects.create(order=final_order, product=product, quantity=quantity,
                                                        price=price,discount =discount,
                                                        sub_total=sub_total, reedem=reedem)
        order_details = OrderSerializer(final_order)
       	return Response({'message': 'Successfully Placed Order',
       			'order_details': order_details.data}, status=200)