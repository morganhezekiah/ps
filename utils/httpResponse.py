from typing import ClassVar


from django.http import JsonResponse

class HttpResponse:
    @staticmethod
    def error( message ):
        return JsonResponse({'message': message}, status=400)
    
    @staticmethod
    def success(message,data = {}):
        return JsonResponse({"message":message, "data":data}, status=200)