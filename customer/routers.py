from rest_framework.routers import DefaultRouter

from .views import (
    CustomerTierViewset,
    CustomerListAPIViewSet,
    CustomerProfileAPIViewSet
)


router = DefaultRouter()
router.register("customer-tier",CustomerTierViewset,basename="customer-tier")
router.register("customer-list", CustomerListAPIViewSet,basename="customers")
router.register("customer-profile",CustomerProfileAPIViewSet,basename="customer-profile")