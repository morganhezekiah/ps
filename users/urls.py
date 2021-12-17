from django.urls import path
from .views import UserSecured, UserUnSecured, Login, UserAccountActivate, CompleteUserAccountActivation
urlpatterns = [
    path("signUp", UserUnSecured.as_view(), name="userSignUp"),
    path("login", Login.as_view()),
    path("delete/<str:userEmail>", UserSecured.as_view()),

    path("user-email-activation/<str:randomString1>/<str:token>/<str:randomString2>", UserAccountActivate),
    path("complete-user-email-activation/<str:token>", CompleteUserAccountActivation)
]
