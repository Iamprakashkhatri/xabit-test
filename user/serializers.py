from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
# from django.contrib.auth.models import User
from rest_framework import serializers,exceptions
from django.contrib.auth.models import Group
from rest_framework.authtoken.serializers import AuthTokenSerializer
# from user.models import User

from .models import *
from customer.models import Customer,CustomerTier

class CustomerSerializer(serializers.ModelSerializer):
    customer_tier_name = serializers.CharField(source="customer_tier.name", read_only=True)
    class Meta:
        model = Customer
        fields = ("customer_id","gender","birth_date","updated_at","created_at","customer_tier_name","customer_tier")
        
        read_only_fields = ("updated_at", "created_at")


class UserSerializer(serializers.ModelSerializer):
    customeruser = CustomerSerializer(required=True)
    class Meta:
        model = User
        fields = ("first_name","last_name","phone_number","is_mobile_app_user","customeruser")
    

class UserEditSerializer(serializers.ModelSerializer):
    customeruser = CustomerSerializer(write_only=True)
    class Meta:
        model = User
        fields = ("first_name","last_name","phone_number","customeruser")
    
    def update(self, instance, validated_data):
        customeruser = []

        instance.customeruser.delete()

        try:
            customeruser = validated_data.pop("customeruser")
        except KeyError:
            raise serializers.ValidationError("Add Customer")
        request = self.context.get("request")

        user, created = User.objects.update_or_create(id=instance.id, defaults=validated_data)
        customeruser = Customer.objects.create(user=user, **customeruser)

        # course.save()
        return user



class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=8, write_only=True,required=True)
    confirm_password = serializers.CharField(write_only=True,required=True)
    customeruser = CustomerSerializer(write_only=True,required=True)
    class Meta:
        model = User
        fields = ("username","first_name","last_name","email","phone_number","password","confirm_password","customeruser","is_mobile_app_user")
        extra_kwargs = {'phone_number': {'required': True}}


    def validate(self, attrs):
        if attrs.get("is_mobile_app_user")==True:
            customer=[]

            if attrs['password'] != attrs['confirm_password']:
                raise serializers.ValidationError(("The two password fields didn't match."))

            if User.objects.filter(phone_number=attrs['phone_number']).exists():
                raise serializers.ValidationError(("This phone_number is already taken"))

            try:
                customeruser = attrs.pop("customeruser")
            except KeyError:
                raise serializers.ValidationError("Add Customer")

            user = User.objects.create(first_name=attrs['first_name'],last_name=attrs['last_name'],
                        phone_number=attrs['phone_number'])
            user.set_password(attrs.get('password'))
            user.save()
            customer=Customer.objects.create(user=user,**customeruser)

            if Group.objects.filter(name="customers").exists():
                user.groups.add(Group.objects.get(name="customers"))
            
            attrs["user"] =user
            return attrs
        else:
            raise serializers.ValidationError("Add yourself a bool value")


class LoginSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField()
    password = serializers.CharField()
    class Meta:
        model = User
        fields = ("phone_number","password")

