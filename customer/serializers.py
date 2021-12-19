from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
# from django.contrib.auth.models import User
from rest_framework import serializers,exceptions
from rest_framework.authtoken.serializers import AuthTokenSerializer
from user.models import User

from .models import (
    CustomerTier,
    Customer,
)

class CustomerTierSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerTier
        fields = "__all__"

class CustomerSerializer(serializers.ModelSerializer):
    customer_tier_name = serializers.CharField(source="customer_tier.name", read_only=True)
    class Meta:
        model = Customer
        fields = ("customer_id","email","gender","birth_date","updated_at","created_at","customer_tier_name","customer_tier")
        
        read_only_fields = ("updated_at", "created_at")



class CustomerRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=8, write_only=True,required=True)
    confirm_password = serializers.CharField(min_length=8, write_only=True,required=True)
    email = serializers.CharField(min_length=8, write_only=True,required=False)
    class Meta:
        model = User
        fields = ("first_name","last_name","email","phone_number","password","confirm_password")

    def validate(self, attrs):
        customer=[]
        customer_tier = attrs.get("customer_tier")

        if customer_tier is None:
            customer_tier,created = CustomerTier.objects.get_or_create(name="general")

        # if User.objects.filter(username=attrs["first_name"],first_name=attrs["first_name"],last_name=attrs["last_name"]).exists():
        #     msg = _("Your name is already taken")
        #     raise serializers.ValidationError(msg, code="authorization")
        # user = User.objects.create(username=attrs["first_name"],first_name=attrs["first_name"],last_name=attrs["last_name"])
        # user.set_password(attrs.get('password'))
        # user.save()

        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError(("The two password fields didn't match."))
        user = User.objects.create(first_name=attrs['first_name'],last_name=attrs['last_name'],
                    phone_number=attrs['phone_number'],email=attrs['email'])
        user.set_password(attrs.get('password'))
        customer=user.save()
        customer=Customer.objects.create(user=user)
        # customer = Customer.objects.create(customer_tier=customer_tier,**attrs)
        # attrs["user"] = user
        attrs["customer"] = customer
        return attrs


class CustomerAuthTokenSerializer(serializers.ModelSerializer):
    username = serializers.CharField(label=_("Username"), write_only=True, required=False)
    password = serializers.CharField(
        label=_("Password"), style={"input_type": "password"}, trim_whitespace=False, write_only=True, required=False
    )

    class Meta:
        model = User
        fields = ("username","password")

    def validate(self, attrs):
        username = attrs.get("username")
        password = attrs.get("password")

        if username and password:
            username = User.objects.get(username=username)
            user = authenticate(request=self.context.get("request"), username=username, password=password)
            print('user',user)
            if not user:
                msg = _("Unable to log in with provided credentials.")
                raise serializers.ValidationError(msg, code="authorization")
        else:
            msg = _('Must include "username" and "password".')
            raise serializers.ValidationError(msg, code="authorization")

        attrs["user"] = user
        return attrs

class LoginSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    password = serializers.CharField()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"