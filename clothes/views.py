import json

from .models import (
    Clothes,
    ClothesColor,
    ClothesImage,
)

from django.views     import View
from django.http      import HttpResponse, JsonResponse

class SubCategoryView(View):
    def get(self, request, gender, clothes_type):
        clothes_list = Clothes.objects.select_related(
            'main_category',
            'sub_category'
        ).filter(main_category = gender, sub_category = clothes_type)

        clothes_image = ClothesImage.objects
        clothes_color = ClothesColor.objects.select_related('color')

        try:
            clothes_lists = [
                {
                    'id '          : result.id,
                    'image'        : clothes_image.filter(clothes_id = result.id)[0].image,
                    'color'        : clothes_color.filter(clothes_id = result.id)[0].color.name,
                    'bestseller'   : result.bestseller,
                    'name'         : result.name,
                    'price'        : result.price,
                    'other_colors' : len(clothes_color.filter(clothes_id = result.id))-1

                }
            for result in clothes_list]

            return JsonResponse({"clothes_list": clothes_lists}, status = 200)

        except KeyError:
            return JsonResponse({"message":"INVALID_KEYS"}, status = 400)
