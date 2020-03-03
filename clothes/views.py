import json

from .models import Clothes, Color

from django.views import View
from django.http  import HttpResponse, JsonResponse

class ClothesDetailView(View):
    def get(self, request, req_clothes_id, req_color_id):
        clothes_detail = Clothes.objects.prefetch_related(
            'clothesimage_set',
            'clothescare_set',
            'clothessize_set').filter(id = req_clothes_id)

        try:
            clothes_details = [{
                'clothes_id'   : req_clothes_id,
                'images'       : list(clothes.clothesimage_set.filter(clothes_id = req_clothes_id, color_id = req_color_id).values_list('image', flat = True)),
                'clothes'      : {"clothes_id"   : req_clothes_id,
                                  "clothes_name" : Clothes.objects.get(id = req_clothes_id).name},
                'price'        : clothes.price,
                'color'        : {"color_id"   : req_color_id,
                                  "color_name" : Color.objects.get(id = req_color_id).name},
                'description'  : clothes.description,
                'size'         : list(clothes.clothessize_set.filter(clothes_id = req_clothes_id).values('size_id', 'size__name')),
                'other_colors' : list(clothes.clothesimage_set.filter(clothes_id = req_clothes_id).values('color__name','image')),
                'composition'  : clothes.composition,
                'care'         : list(clothes.clothescare_set.filter(clothes_id = req_clothes_id).values('care__name', flat = True))
            } for clothes in clothes_detail]

            return JsonResponse({"clothes_details": clothes_details}, status = 200)

        except KeyError:
            return JsonResponse({"message": "INVALID_KEYS"}, status = 400)
