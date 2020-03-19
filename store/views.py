import json

from .models import Store

from django.views import View
from django.http  import HttpResponse,JsonResponse

from haversine import haversine

class MapView(View):
    def post(self, request):
        map_data           = json.loads(request.body)
        map_data_province  = map_data.get('province'  , None)
        map_data_longitude = map_data.get('longitude' , None)
        map_data_latitude  = map_data.get('latitude'  , None)

        try:
            if Store.objects.filter(address__contains = map_data_province).exists():
               store_list = Store.objects.filter(address__contains=map_data_province).values()
               return JsonResponse({"all_data":list(store_list)}, status = 200)
            else:
                stores = (
                    Store
                    .objects
                    .filter(latitue >= 100, longtitude >= 100)
                    .values('name', 'address', 'latitude', 'longitudue')
                )

                return JsonResponse({'map data':stores},status=200)
        except KeyError:
            return JsonResponse({'msg':'Key Error'},status=400)
