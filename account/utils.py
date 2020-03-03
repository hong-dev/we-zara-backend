import jwt
import json

from .models import Account
from zara.settings import SECRET_KEY

from django.http import JsonResponse


def login_required(func):

   def wrapper(self, request, *args, **kwargs):
       access_token = request.headers.get('Authorization', None)
       secret = SECRET_KEY['secret']
       if access_token:
           try:
                decode = jwt.decode(access_token, secret, algorithms=['HS256'])
                user_email = decode.get('email', None)
                user = Account.objects.get(email=user_email)

                request.user = user

           except jwt.DecodeError:
               return JsonResponse({"message" : "잘못된 토큰 입니다."}, status = 403)
           except Account.DoesNotExist:
               return JsonResponse({"message" : "존재하지 않는 아이디 입니다."}, status=401)
           return func(self, request, *args, **kwargs)

       return JsonResponse({"message" : "로그인이 필요한 서비스 입니다."}, status=401)

   return wrapper


