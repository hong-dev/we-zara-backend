import json

from .models import Store

from django.views import View
from django.http  import HttpResponse,JsonResponse

from haversine import haversine

class ShowMap(View):
    def post(self, request):
        map_data           = json.loads(request.body)
        map_data_province  = map_data.get('province',None)
        map_data_longitude = map_data.get('longitude',None)
        map_data_latitude  = map_data.get('latitude',None)

        if map_data_latitude and map_data_longitude and map_data_province:
            if Store.objects.filter(address__contains = map_data_province).exists():
               store_list = Store.objects.filter(address__contains=map_data_province).values()
               return JsonResponse({"all_data":list(store_list)}, status = 200)
            else:
                target=(float(map_data_latitude),float(map_data_longitude))
                stores=[]
                for element in Store.objects.all():
                    store=(float(element.latitude),float(element.longitude))
                    if haversine(target,store)<100:
                        stores.append({
                            'name'     :element.name,
                            'address'  :element.address,
                            'latitude' :element.latitude,
                            'longitude':element.longitude
                        })
                if len(stores) < 1:
                    return JsonResponse({'msg':'No Data'},status=200)
                return JsonResponse({'map data':stores},status=200)
        return JsonResponse({'msg':'Key Error'},status=400)
