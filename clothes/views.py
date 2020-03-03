import json

from .models import Clothes, Color, ClothesImage

from django.views import View
from django.http  import HttpResponse, JsonResponse

class SubCategoryView(View):
    def get(self, request, gender, clothes_type):
        clothes_list = ClothesImage.objects.select_related('clothes').filter(
            clothes__main_category_id = gender,
            clothes__sub_category_id  = clothes_type
        )

        try:
            clothes_lists = [
                {
                    'id '          : result.clothes.id,
                    'image'        : result.main_image,
                    'color'        : result.color_id,
                    'new'          : result.clothes.new,
                    'name'         : result.clothes.name,
                    'price'        : result.clothes.price,
                    'other_colors' : len(clothes_list.filter(clothes_id = result.clothes_id))-1
                } for result in clothes_list]

            return JsonResponse({"clothes_list": clothes_lists}, status = 200)

        except KeyError:
            return JsonResponse({"message":"INVALID_KEYS"}, status = 400)

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