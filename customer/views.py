from django.http import HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

from django_filters.rest_framework import DjangoFilterBackend
from django.core.exceptions import ObjectDoesNotExist

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

from user.serializers import UserSerializer,UserEditSerializer

from .models import CustomerTier,Customer
from .serializers import (
	CustomerTierSerializer,
    CustomerSerializer,
    CustomerRegisterSerializer,
    CustomerAuthTokenSerializer
)


class CustomerTierViewset(viewsets.ModelViewSet):
    """
    Customer Tier Listing API
    """

    permission_classes = (IsAuthenticated,)
    serializer_class = CustomerTierSerializer
    queryset = CustomerTier.objects.all().order_by('-id')

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        obj=serializer.save()
        return Response({"message": f"{obj.name} Customer Tier Successfully Added", "data": serializer.data}, status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        obj = self.get_object()
        serializer = self.get_serializer(obj, data=request.data)
        serializer.is_valid(raise_exception=True)
        obj = serializer.save()
        return Response({"message": f"{obj.name} Customer Tier Successfully Edited", "data": serializer.data}, status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        name = instance.name
        self.perform_destroy(instance)
        return Response({"message": f"{name} Customer Tier Successfully"}, status.HTTP_204_NO_CONTENT)



class CustomerListAPIViewSet(viewsets.ModelViewSet):
    serializer_class = CustomerSerializer
    permission_classes = (IsAdminUser,)
    queryset = Customer.objects.all()
    http_method_names = [
        "get",
        "put",
        "patch",
    ]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ["is_active",]
    search_fields = ["first_name", "email","phone_number"]

    def update(self, request, *args, **kwargs):
        obj = self.get_object()
        serializer = self.get_serializer(obj, data=request.data)
        if serializer.is_valid(raise_exception=True):
            customer = serializer.save()
            return Response({"message": f"{customer.first_name} Customer Successfully Edited", "data": serializer.data}, status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=400)


class CustomerProfileAPIViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)
    queryset = Customer.objects.none()
    http_method_names = [
        "get",
        "put",
        "patch",
    ]

    def get_object(self, queryset=None):
        return User.objects.get(id=self.request.user.id)

    def paginate_queryset(self, queryset):
        return None

    def update(self, request, *args, **kwargs):
        obj = self.get_object()
        serializer = self.get_serializer(obj, data=request.data)
        if serializer.is_valid(raise_exception=True):
            customer = serializer.save()
            return Response({"message": f"{customer.first_name} Your Profile Successfully Edited", "data": serializer.data}, status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=400)


class CustomerProfileUpdateView(APIView):
    serializer_class = UserEditSerializer
    permission_classes = [
        IsAuthenticated,
    ]

    def post(self, request, *args, **kwargs):
        print(request, type(request))
        user = User.objects.get(id=kwargs["id"])
        if not user:
            return Response({"message": "Could not update ID not provided"})
        serializer = UserEditSerializer(data=request.data, context={"request": self.request}, instance=user)
        if not serializer.is_valid(raise_exception=True):
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        obj = serializer.save()
        return Response(
            {"message": "Success", "data": UserSerializer(obj, context={"request": self.request}).data},
            status.HTTP_200_OK,
        )

from .serializers import *
class RegisterCustomerAPIView(CreateAPIView):
    """
    API View for registration.
    """

    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        serializer = CustomerRegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        customer = serializer.validated_data["customer"]
        data = UserSerializer(customer).data
        refresh = RefreshToken.for_user(customer)
        return Response(
            {
                "message": "Success",
                "token": str(refresh),
                "access": str(refresh.access_token),
                "customer": data,
            },
            status.HTTP_201_CREATED,
        )


# class LoginAPIView(APIView):

#     def post(self, request, *args, **kwargs):
#         first_name = request.data.get('first_name')
#         phone_number = request.data.get('phone_number')
#         if not first_name:
#             return Response({'message': "first_name not provided"}, status=400)
#         if not phone_number:
#             return Response({'message': "phone_number not provided"}, status=400)
#         try:
#             customer = Customer.objects.get(first_name=first_name, phone_number=phone_number)
#             if not customer.is_active:
#                 return Response({'message': 'You have been blocked from the site. Please contact the Management'})

#             refresh = RefreshToken.for_user(customer)
#             # token = 
#             customer_serializer = CustomerSerializer(customer)
#             # token = MyOwnToken.objects.get(customer=customer).key
#             return Response(
#                 {
#                     "message": "Success",
#                     "token": str(refresh),
#                     "access": str(refresh.access_token),
#                     "customer": customer_serializer.data,
#                 },
#                 status.HTTP_200_OK,
#             )

#             # return Response({'token': jwt_encode_handler(payload), 'user': data}, status=200)

#         except ObjectDoesNotExist:
#             return Response({'message': "Customer Does not exists"}, status=400)


# class ObtainAuthTokenView(ObtainAuthToken):
#     serializer_class = CustomerAuthTokenSerializer

#     def post(self, request):
#         serializer = self.serializer_class(data=request.data)
#         try:
#             username = serializer.initial_data["username"]
#             user = get_object_or_404(User, username=username)
#             if not user.is_active:
#                 return Response(
#                     {
#                         "message": "You account is currently under review. It will be activated real soon by Homework Team."
#                     },
#                     status.HTTP_200_OK,
#                 )
#         except:
#             pass
#         serializer.is_valid(raise_exception=True)
#         user = serializer.validated_data["user"]
#         refresh = RefreshToken.for_user(user)
#         user_serializer = CustomerSerializer(user)
#         return Response(
#             {
#                 "message": "Success",
#                 "refresh": str(refresh),
#                 "access": str(refresh.access_token),
#                 "user": user_serializer.data,
#             },
#             status.HTTP_200_OK,
#         )

from .serializers import LoginSerializer,UserSerializer
from django.contrib.auth import authenticate

class LoginAPIView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            phone_number = serializer.data['phone_number']
            password = serializer.data['password']
            user = authenticate(phone_number=phone_number, password=password)
            if user:
                if Customer.objects.filter(phone_number=phone_number).exists():
                    customer = Customer.objects.get(phone_number=phone_number)
                    refresh = RefreshToken.for_user(customer)
                    customer_serializer = CustomerSerializer(customer).data
                    return Response(
                        {
                            "message": "Success",
                            "token": str(refresh),
                            "access": str(refresh.access_token),
                            "customer": customer_serializer,
                        },
                        status.HTTP_200_OK,
                    )
                else:
                    return Response({'error':"Your are not customer"},status=400)
            return Response({'error':"Invalid Credentials"},status=400)
        return Response(serializer.errors, status=400) 
