import json

from .models import Store

from django.views import View
from django.http  import HttpResponse,JsonResponse


class ShowMap(View):
    def get(self, request):
        store_list = Store.objects.values()

        return JsonResponse({"all_data":list(store_list)}, status = 200)
