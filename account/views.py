import json
import bcrypt
import jwt

from zara.settings import SECRET_KEY
from .models       import Account

from django.views           import View
from django.http            import HttpResponse, JsonResponse
from django.core.validators import EmailValidator
from django.core.exceptions import ValidationError


class SignupView(View):
    def post(self, request):
        account_data = json.loads(request.body)
        validator = EmailValidator()

        if Account.objects.filter(email = account_data['email']).exists():
            return JsonResponse({"message":"EMAIL_ALREADY_EXISTS"}, status = 400)

        try:
            validator(account_data['email'])

            Account(
                email    = account_data['email'],
                password = bcrypt.hashpw(account_data['password'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8'),
                name     = account_data['name'],
                address  = account_data['address'],
                country  = account_data['country'],
                phone    = account_data['phone'],
            ).save()
            return HttpResponse(status = 200)

        except ValidationError:
                return JsonResponse({"message":"EMAIL_VALIDATION_ERROR"}, status = 422)

        except KeyError:
            return JsonResponse({"message":"INVALID_KEYS"}, status = 400)

class SigninView(View):
    def post(self, request):
        account_data = json.loads(request.body)

        try:
            if Account.objects.filter(email = account_data['email']).exists():
                account = Account.objects.get(email = account_data['email'])

                if bcrypt.checkpw(account_data['password'].encode('utf-8'), account.password.encode('utf-8')):
                    token = jwt.encode({'email': account.email}, SECRET_KEY['secret'], algorithm = 'HS256').decode('utf-8')
                    return JsonResponse({"token" : token}, status = 200)

                return HttpResponse(status = 401)

            return HttpResponse(status = 400)

        except KeyError:
            return JsonResponse({"message":"INVALID_KEYS"}, status = 400)

