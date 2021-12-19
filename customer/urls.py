from django.urls import path,include
from .routers import router


from .views import (
    CustomerProfileAPIViewSet,
    CustomerProfileUpdateView,
    # RegisterCustomerAPIView,
    # LoginAPIView
)

app_name = 'customer'

urlpatterns = [
    path('', include(router.urls)),
    path('customer-profile/<pk>/', CustomerProfileAPIViewSet.as_view({
    'get': 'retrieve',
    'put': 'update'
    })),
    path("update/<int:id>/", CustomerProfileUpdateView.as_view()),
    # path("register/", RegisterCustomerAPIView.as_view(), name="register"),
    # path("login/", LoginAPIView.as_view()),
]
