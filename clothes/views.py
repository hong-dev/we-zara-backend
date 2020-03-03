import json

from .models import Clothes, Color, ClothesImage

from django.views import View
from django.http  import HttpResponse, JsonResponse

class ClothesDetailView(View):
    def get(self, request, req_clothes_id, req_color_id):
        try:
            clothes_detail = Clothes.objects.prefetch_related(
                'clothesimage_set',
                'clothescare_set',
                'clothessize_set').filter(id = req_clothes_id)

            color_name   = Color.objects.get(id = req_color_id).name
            clothes_name = Clothes.objects.get(id = req_clothes_id).name

            clothes_details = [{
                'clothes_id'   : req_clothes_id,
                'images'       : list(clothes.clothesimage_set.filter(color_id = req_color_id).values(
                    'main_image', 'image1', 'image2', 'image3', 'image4', 'image5', 'image6', 'image7')),
                'clothes'      : {"clothes_id"   : req_clothes_id, "clothes_name" : clothes_name},
                'price'        : clothes.price,
                'color'        : {"color_id"   : req_color_id, "color_name" : color_name},
                'description'  : clothes.description,
                'size'         : list(clothes.clothessize_set.values('size_id', 'size__name')),
                'other_colors' : list(clothes.clothesimage_set.values('color__name','image')),
                'composition'  : clothes.composition,
                'care'         : list(clothes.clothescare_set.values('care__name', flat = True))
            } for clothes in clothes_detail]

            return JsonResponse({"clothes_details": clothes_details}, status = 200)

        except KeyError:
            return JsonResponse({"message": "INVALID_KEYS"}, status = 400)

class SubCategoryView(View):
    def get(self, request, gender, clothes_type):
        try:
            clothes_list = ClothesImage.objects.select_related('clothes').filter(
            clothes__main_category_id = gender,
            clothes__sub_category_id  = clothes_type
        )

            clothes_lists = [
                {
                    'id '          : result.clothes.id,
                    'image'        : result.main_image,
                    'color'        : result.color_id,
                    'new'          : result.clothes.new,
                    'name'         : result.clothes.name,
                    'price'        : result.clothes.price,
                    'other_colors' : len(clothes_list.filter(clothes_id = result.clothes_id))-1
                }
            for result in clothes_list]

            return JsonResponse({"clothes_list": clothes_lists}, status = 200)

        except KeyError:
            return JsonResponse({"message":"INVALID_KEYS"}, status = 400)
