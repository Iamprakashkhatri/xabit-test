from django.urls import path,include
# from .routers import router


from .views import (
    RegisterUserAPIView,
    LoginAPIView
)

app_name = 'user'

urlpatterns = [
    # path('', include(router.urls)),
    path("register/", RegisterUserAPIView.as_view(), name="register"),
    path("login/", LoginAPIView.as_view()),
]
