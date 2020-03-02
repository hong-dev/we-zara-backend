import json

from .models import (
    Clothes,
    ClothesColor,
    ClothesImage,
    ClothesCare,
    ClothesSize
)

from django.views import View
from django.http  import HttpResponse, JsonResponse

class ClothesDetailView(View):
    def get(self, request, req_clothes_id, req_color_id):
        clothes_detail = Clothes.objects.filter(id = req_clothes_id)[0]

        clothes_image = ClothesImage.objects
        clothes_color = ClothesColor.objects.select_related('color').filter(clothes_id = req_clothes_id)
        clothes_care  = ClothesCare.objects.select_related('care').filter(clothes_id = req_clothes_id)
        clothes_size  = ClothesSize.objects.select_related('size').filter(clothes_id = req_clothes_id)

        try:
            clothes_details = {
                    'images'       : clothes_image.get(
                        clothes_id = req_clothes_id,
                        color_id   = req_color_id
                    ).image,
                    'name'         : clothes_detail.name,
                    'price'        : clothes_detail.price,
                    'color'        : clothes_color.get(
                        color_id   = req_color_id
                    ).color.name,
                    'other_colors' : [element.color.name for element in clothes_color],
                    'description'  : clothes_detail.description,
                    'size'         : [element.size.name for element in clothes_size],
                    'composition'  : clothes_detail.composition,
                    'care'         : [element.care.name for element in clothes_care]
                }
            clothes_details['other_colors'].remove(clothes_details['color'])
            return JsonResponse({"clothes_details": clothes_details}, status = 200)

        except ClothesImage.DoesNotExist:
            return JsonResponse({"message": "INVALID_VALUE"}, status = 400)

        except ClothesColor.DoesNotExist:
            return JsonResponse({"message": "INVALID_VALUE"}, status = 400)

        except KeyError:
            return JsonResponse({"message": "INVALID_KEYS"}, status = 400)
