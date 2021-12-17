from rest_framework.views import APIView
from django.http import JsonResponse
from .models import User
from .serializers import UserSerializer
from utils.httpResponse import HttpResponse
from utils.RandomStrings import GenerateRandomString
from django.contrib.auth.hashers import make_password, check_password
from knox.models import AuthToken
from django.utils.html import strip_tags
from django.template.loader import render_to_string
from django.shortcuts import render 
from threading import Thread
from django.core.mail import EmailMultiAlternatives
from django.contrib.sites.shortcuts import get_current_site
from utils.JWTTokenManager import UserTokenManager


class UserUnSecured(APIView):
    def get(self, request):
        s = UserSerializer(User.object.all(), many=True)
        return HttpResponse.success("User", data={"morgan":"dhdd"})
    
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")
        if not email:
            return HttpResponse.error("Please enter an email")
        if not password:
            return HttpResponse.error("Please enter a password")

        try:
            u = User.object.get(email=email)
            return HttpResponse.error("Email already registered")
        except User.DoesNotExist as e:
            pass
        


        data ={"email":email,"password":make_password(password),"slug":GenerateRandomString.randomStringGenerator(40)}
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            u = User.object.get(email=email)
            data = {
                "user":serializer.validated_data,
                "token":AuthToken.objects.create(u)[1]
            }
            sendUserAcctEmail = Thread(target=sendUserAccountActivationEmail, args=(request,u))
            sendUserAcctEmail.start()
            return HttpResponse.success("User created successfully", data)
        else:
            return JsonResponse({"message":"Error registering User", "data":serializer.errors},status=400)

        




class UserSecured(APIView):
    def delete(self, request, userEmail):
        try:
            u =User.object.get(email=userEmail)
            s = UserSerializer(u)
            u.delete()
            return HttpResponse.success("User account deleted successfully", s.data)
        except User.DoesNotExist as e:
            return HttpResponse.error("User email is not registered")
    
    def get(self, request, userEmail):
        try:
            u =User.object.get(email=userEmail)
            s = UserSerializer(u)
            return HttpResponse.success("User account retrieved successfully", s.data)
        except User.DoesNotExist as e:
            return HttpResponse.error("User email is not registered")




class Login(APIView):
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")
        if not email:
            return HttpResponse.error("Please enter an email")
        if not password:
            return HttpResponse.error("Please enter a password")

        try:
            u = User.object.get(email=email)
            if u.email == email:
                if check_password(password, u.password):
                    token = AuthToken.objects.create(u)
                    data ={
                        "user": UserSerializer(u).data,
                        "token":token[1]
                    }
                    if u.is_active:
                        return HttpResponse.success("User LoggedIn Successfully", data)
                    else:
                        return HttpResponse.error("User account not activated")
            else:
                return HttpResponse.error("Email is not correct, try again")


        except User.DoesNotExist as e:
            return HttpResponse.error("User with this email does not exist.")

def UserAccountActivate(request, randomString1,token,randomString2):
    return render(request, "users/userAccountActivate.html", {"token":token})

def CompleteUserAccountActivation(request, token):
    tokenManager = UserTokenManager()
    res = tokenManager.decodeToken(token)
    if  res.get("state"):
        u = res.get("user")
        u.is_active = True
        u.save()
        return HttpResponse.success("User account activated succesfully",{"user":UserSerializer(u).data})
    else:
        return HttpResponse.error(res.get("message"))

def sendUserAccountActivationEmail(request, user):
    tokenGen = UserTokenManager()
    activationLink = "http://"+get_current_site(request).domain+"/user/user-email-activation/"+GenerateRandomString.randomStringGenerator(40)+"/"+tokenGen.generateToken(user)+"/"+GenerateRandomString.randomStringGenerator(20)
    html_content = render_to_string('emails/userCreatedEmail.html', {'activationLink':activationLink})
    text_content = strip_tags(html_content)
    subject = "User Account Activation"
    from_email= "PS"
    msg = EmailMultiAlternatives(subject, text_content, from_email, ["morganhezekiah11@gmail.com",user.email])
    msg.attach_alternative(html_content, "text/html")
    msg.send()




def test(request):
    activationLink = "https://mail.google.com/mail/u/0/#inbox/FMfcgzGllMLLGqCKvHfJfxXVVjlWNTlV"
    user = User.object.first()
    ##sendUserAccountActivationEmail(request, user)
    return render(request, 'users/userAccountActivate.html', {'activationLink':activationLink})