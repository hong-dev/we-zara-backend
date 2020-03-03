import json

from .models import (
    ClothesImage,
)

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
                }
            for result in clothes_list]

            return JsonResponse({"clothes_list": clothes_lists}, status = 200)

        except KeyError:
            return JsonResponse({"message":"INVALID_KEYS"}, status = 400)
