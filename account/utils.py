import jwt
import json

from .models       import Account
from zara.settings import SECRET_KEY

from django.http   import JsonResponse


def login_required(func):

   def wrapper(self, request, *args, **kwargs):
       access_token = request.headers.get('Authorization', None)
       if access_token:
           try:
                decode = jwt.decode(access_token, SECRET_KEY['secret'], algorithms=['HS256'])
                user = Account.objects.get(email=decode['email'])
                request.user = user

           except jwt.DecodeError:
               return JsonResponse({"msg" : "Invalid token"}, status = 403)

           except Account.DoesNotExist:
               return JsonResponse({"msg" : "Account does not exist"}, status=401)
           
           return func(self, request, *args, **kwargs)
       
       return JsonResponse({"msg" : "You need to login"}, status=401)
   return wrapper


