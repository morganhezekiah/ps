from rest_framework.views import APIView
from django.http import JsonResponse
from rest_framework import permissions


from utils.httpResponse import HttpResponse
from .serializers import PasswordSerializer
from .models import Passwords

class Password(APIView):
    permission_classes =[ permissions.IsAuthenticated]
    def get(self, request):
        user = self.request.user
        p =Passwords.objects.filter(user=user)
        serializer = PasswordSerializer(p, many=True)
        res ={
            "passwords":serializer.data,
            "count":len(serializer.data),
            "message":"Passwords retrieved successfully"
        }

        return JsonResponse(res,safe=False)
    
    def post(self, request):
        value = request.data.get("value")
        acct = request.data.get("acct")
        acct_id = request.data.get("acct_id")

        if not value :
            return HttpResponse.error("Please enter the password value")
        if not acct:
            return HttpResponse.error("Please enter the password account")
        if not acct_id:
            return HttpResponse.error("Please enter the password ID")

        
        acct = acct.upper()
        data = {
            "acount_name":acct,
            "value":value,
            "value_id":acct_id,
            "user":self.request.user.pk
        }

        try:
            Passwords.objects.get(user=self.request.user.pk, acount_name=acct)
            return HttpResponse.error("User has a password with this account name already")
        except Exception as e:
            pass

        serializer = PasswordSerializer(data=data)
        
        if serializer.is_valid():
            serializer.save()
            responseSer = PasswordSerializer(Passwords.objects.get(user=self.request.user.pk, acount_name=acct))
            res ={
                "password":responseSer.data
            }
            return HttpResponse.success("Password created successfully", res)
        else:
            return JsonResponse({"message":"Error creating password, please try again","data":serializer.errors}, status=400)
    def delete(self, request, pId):
        try:
            p= Passwords.objects.get(id=pId)
            serializer= PasswordSerializer(p)
            p.delete()
            res ={
                "message":"Password deleted successfully",
                "password":serializer.data
            }
            return JsonResponse(res, status=200)
        except Passwords.DoesNotExist as e:
            return HttpResponse.error("Password with this ID does not exist")

    def put(self, request, pId):
        value = request.data.get("value")
        acct = request.data.get("acct")
        acct_id = request.data.get("acct_id")
        print(acct)

        if not value :
            return HttpResponse.error("Please enter the password value")
        if not acct:
            return HttpResponse.error("Please enter the password account")
        if not acct_id:
            return HttpResponse.error("Please enter the password ID")

        
        acct = acct.upper()
        data = {
            "acount_name":acct,
            "value":value,
            "value_id":acct_id,
            "user":self.request.user.pk
        }

        try :
            p = Passwords.objects.get(id=pId)
        except Passwords.DoesNotExist as e:
            return HttpResponse.error("Password with this ID does not exist")
        
        if p.acount_name  != acct:
            try:
                Passwords.objects.get(user=self.request.user.pk, acount_name=acct)
                return HttpResponse.error("User has a password with this account name already")
            except Exception as e:
                pass

        serializer = PasswordSerializer(p,data= data)
        if serializer.is_valid():
            serializer.save()
            serializer.validated_data["user"] = self.request.user.pk
            serializer = PasswordSerializer(Passwords.objects.get(user=self.request.user.pk, acount_name=acct))
            data ={
                "password":serializer.data
            }
            return HttpResponse.success("Password editted successfully",data)
        else:
            return JsonResponse({"message":"Error editting password,please try again"})
