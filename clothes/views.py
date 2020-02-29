import json

from .models import (
    MainCategory,
    SubCategory,
    Clothes,
    ClothesColor,
    ClothesImage
)

from django.views     import View
from django.http      import HttpResponse, JsonResponse
from django.db.models import Count

class SubCategoryView(View):
    def get(self, request, gender, clothes_type):
        if MainCategory.objects.filter(id = gender).exists() and SubCategory.objects.filter(id = clothes_type).exists():
            related_clothes = Clothes.objects.select_related('main_category', 'sub_category')
            filter_clothes = related_clothes.filter(main_category__id = gender, sub_category__id = clothes_type)

            related_clothes_2 = filter_clothes.prefetch_related('color', 'clothesimage_set')
            added_color = related_clothes_2.annotate(color_count = Count('clothescolor__clothes_id'))

            result_clothes = added_color.values(
                'bestseller',
                'color_count',
                'name',
                'price',
            )
            return JsonResponse({"clothes_list": list(result_clothes)}, status = 200)

        return HttpResponse(status = 404)
