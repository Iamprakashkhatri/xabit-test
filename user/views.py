from django.http import HttpResponse
from django.contrib.auth.models import User
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

from .models import User
from .serializers import UserRegisterSerializer,UserSerializer,LoginSerializer


class RegisterUserAPIView(CreateAPIView):
    """
    API View for registration.
    """

    serializer_class = UserRegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = UserRegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        data = UserSerializer(user).data
        refresh = RefreshToken.for_user(user)
        return Response(
            {
                "message": "Success",
                "token": str(refresh),
                "access": str(refresh.access_token),
                "customer": data,
            },
            status.HTTP_201_CREATED,
        )


class LoginAPIView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            phone_number = serializer.data['phone_number']
            print('phone_number',phone_number)
            password = serializer.data['password']
            print('password',password)
            user=User.objects.get(phone_number=phone_number)
            user = authenticate(username=user.username, password=password)

            if user:
                refresh = RefreshToken.for_user(user)
                customer_serializer = UserSerializer(user).data
                return Response(
                    {
                        "message": "Success",
                        "token": str(refresh),
                        "access": str(refresh.access_token),
                        "customer": customer_serializer,
                    },
                    status.HTTP_200_OK,
                )
                # else:
                #     return Response({'error':"Your are not customer"},status=400)
            return Response({'error':"Invalid Credentials"},status=400)
        return Response(serializer.errors, status=400) 
