import json

from .models import Store

from django.views import View
from django.http  import HttpResponse,JsonResponse

from haversine import  haversine

class ShowMap(View):
    def post(self, request):
        map_data = json.loads(request.body)
        
        if Store.objects.filter(address__contains = map_data['province']).exists():
            store_list = Store.objects.filter(address__contains=map_data['province']).values()
            return JsonResponse({"all_data":list(store_list)}, status = 200)
        
        else:
            target=(float(map_data['latitude']),float(map_data['longitude']))
            stores=[]
            for element in Store.objects.all():
                store=(float(element.latitude),float(element.longitude))
                if haversine(target,store)<100 :
                    stores.append({
                        'name'     :element.name,
                        'address'  :element.address,
                        'latitude' :element.latitude,
                        'longitude':element.longitude
                    } )
            return JsonResponse({'map data':stores},status=200)



        return JsonResponse({"No DATA":"0"},status=400)
