
from django.urls import path

from passwords.views import Password


urlpatterns = [
    path('', Password.as_view()),
    path('<pId>', Password.as_view())
]
