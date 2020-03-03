import json

from .models import Clothes, Color, ClothesImage, New

from django.views import View
from django.http  import HttpResponse, JsonResponse

class SubCategoryView(View):
    def get(self, request, gender, clothes_type):
        try:
            clothes_list = ClothesImage.objects.select_related('clothes').filter(
            clothes__main_category_id = gender,
            clothes__sub_category_id  = clothes_type
        )

            clothes_lists = [
                {
                    'id '          : result.clothes_id,
                    'image'        : result.main_image,
                    'color'        : result.color_id,
                    'new'          : result.clothes.is_new,
                    'name'         : result.clothes.name,
                    'price'        : result.clothes.price,
                    'other_colors' : len(clothes_list.filter(clothes_id = result.clothes_id))-1
                } for result in clothes_list]

            return JsonResponse({"clothes_list": clothes_lists}, status = 200)

        except KeyError:
            return JsonResponse({"message":"INVALID_KEYS"}, status = 400)

class ClothesNewView(View):
    def get(self, request, gender):
        try:
            clothes_list = ClothesImage.objects.select_related('clothes').filter(
                clothes__main_category_id = gender,
                clothes__is_new           = True
             )

            clothes_new = New.objects.select_related('main_category').filter(main_category_id = gender)

            marketing_list = list(clothes_new.values_list('image', flat = True))

            new_list = [
                {
					'id'           : result.clothes_id,
                    'image'        : result.main_image,
                    'color'        : result.color_id,
                    'new'          : result.clothes.is_new,
                    'name'         : result.clothes.name,
                    'price'        : result.clothes.price,
                    'other_colors' : len(clothes_list.filter(clothes_id = result.clothes_id))-1
                } for result in clothes_list]

            return JsonResponse({"marketing": marketing_list, "new": new_list}, status = 200)

        except KeyError:
            return JsonResponse({"message":"INVALID_KEYS"}, status = 400)

class ClothesDetailView(View):
    def get(self, request, req_clothes_id, req_color_id):
        try:
            if not ClothesImage.objects.filter(clothes_id = req_clothes_id, color_id = req_color_id).exists():
                return HttpResponse(status = 404)

            clothes_detail = Clothes.objects.prefetch_related(
                'clothesimage_set',
                'clothescare_set',
                'clothessize_set').filter(id = req_clothes_id)

            color_name   = Color.objects.get(id = req_color_id).name
            clothes_name = Clothes.objects.get(id = req_clothes_id).name

            clothes_details = [{
                'images'       : list(clothes.clothesimage_set.filter(color_id = req_color_id).values(
                    'main_image', 'image1', 'image2', 'image3', 'image4', 'image5', 'image6', 'image7')),
                'clothes'      : {"clothes_id"   : req_clothes_id, "clothes_name" : clothes_name},
                'price'        : clothes.price,
                'color'        : {"color_id"   : req_color_id, "color_name" : color_name},
                'description'  : clothes.description,
                'size'         : list(clothes.clothessize_set.values('size_id', 'size__name')),
                'other_colors' : list(clothes.clothesimage_set.values('color__name','image7')),
                'composition'  : clothes.composition,
                'care'         : list(clothes.clothescare_set.values_list('care__name', flat = True))
            } for clothes in clothes_detail]

            return JsonResponse({"clothes_details": clothes_details}, status = 200)

        except KeyError:
            return JsonResponse({"message": "INVALID_KEYS"}, status = 400)

class SearchView(View):
    def get(self, request):
        try:
            keyword = request.GET.get('keyword', None)

            clothes_list = ClothesImage.objects.select_related('clothes').filter(clothes__name__contains = keyword)

            result_list = [
                {
                    'id'           : result.clothes_id,
                    'image'        : result.main_image,
                    'color'        : result.color_id,
                    'new'          : result.clothes.is_new,
                    'name'         : result.clothes.name,
                    'price'        : result.clothes.price,
                    'other_colors' : len(clothes_list.filter(clothes_id = result.clothes_id))-1
                } for result in clothes_list]

            if len(result_list) == 0:
                return JsonResponse({"message": "ITEM_DOES_NOT_EXIST"}, status = 400)

            return JsonResponse({"results": result_list}, status = 200)

        except KeyError:
            return JsonResponse({"message": "INVALID_KEYS"}, status = 400)
