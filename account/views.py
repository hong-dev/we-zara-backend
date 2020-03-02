import json
import bcrypt
import jwt

from zara.settings import SECRET_KEY
from .models       import Account

from django.views           import View
from django.http            import HttpResponse, JsonResponse
from django.db              import IntegrityError
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

class SignupView(View):
    def post(self, request):
        account_data = json.loads(request.body)

        try:
            if account_data['phone'].isdigit() == False:
                return JsonResponse({"message":"PHONE_VALIDATION_ERROR"}, status = 400)
            if (len(account_data['password']) < 8 or
                account_data['password'].islower() or
                account_data['password'].isupper() or
                account_data['password'].isdigit() or
                account_data['password'].isalpha()):
                return JsonResponse({"message":"PASSWORD_VALIDATION_ERROR"}, status = 400)

            validate_email(account_data['email'])

            Account(
                email    = account_data['email'],
                password = bcrypt.hashpw(account_data['password'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8'),
                name     = account_data['name'],
                address  = account_data['address'],
                country  = account_data['country'],
                phone    = account_data['phone'],
            ).save()
            return HttpResponse(status = 200)

        except IntegrityError:
            return JsonResponse({"message":"EMAIL_ALREADY_EXISTS"}, status = 400)

        except ValidationError:
            return JsonResponse({"message":"EMAIL_VALIDATION_ERROR"}, status = 400)

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
