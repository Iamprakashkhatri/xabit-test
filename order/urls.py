from django.urls import include, path

# from .routers import router
from .views import *

app_name = "order"

urlpatterns = [
    # path("", include(router.urls)),
    path("create-order/", OrderCreateAPI.as_view(), name="create-order")
]
