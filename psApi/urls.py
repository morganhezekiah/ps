
from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from users.views import test


urlpatterns = [
    path('admin/', admin.site.urls),
    path("password/", include("passwords.urls")),
    path("user/", include("users.urls")),
    path("test", test, name="test")
]
