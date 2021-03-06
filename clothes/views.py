import json
import random
import collections

from .models import Clothes, Color, Size, ClothesImage, New

from ast          import literal_eval
from django.views import View
from django.http  import HttpResponse, JsonResponse

def extract_data(field_name, deduplicated_list):
    field_spec      = collections.namedtuple(field_name, "id, name")
    namedtuple_list = [field_spec(element[0], element[1]) for element in deduplicated_list]
    dict_field      = [dict(tuples._asdict()) for tuples in namedtuple_list]

    return dict_field

class SubCategoryView(View):
    def get(self, request, gender, clothes_type):
        try:
            clothes_list = ClothesImage.objects.select_related('clothes').filter(
                clothes__main_category_id = gender,
                clothes__sub_category_id  = clothes_type
            ).order_by('clothes__price')

            deduplication_color = sorted(set([(clothes.color.id, clothes.color.name) for clothes in clothes_list]))

            size_list = Size.objects.prefetch_related('clothes_set').filter(
                clothes__main_category_id = gender,
                clothes__sub_category_id = clothes_type
            )
            deduplication_size = sorted(set([(size.id, size.name) for size in size_list]))

            price_list = [price for price in range(round(clothes_list[0].clothes.price + 5000, -4),
                                                   round(clothes_list[len(clothes_list)-1].clothes.price + 35000, -4), 30000)]

            filter_list = {
                'colors' : extract_data("colors", deduplication_color),
                'sizes'  : extract_data("sizes", deduplication_size),
                'prices' : [{"id": index, "name": value} for index, value in enumerate(price_list)]
            }

            clothes_lists = [
                {
                    'id '          : result.clothes.id,
                    'image'        : result.image1,
                    'color'        : result.color_id,
                    'new'          : result.clothes.is_new,
                    'name'         : result.clothes.name,
                    'price'        : result.clothes.price,
                    'other_colors' : len(clothes_list.filter(clothes_id = result.clothes_id))-1
                } for result in clothes_list]

            return JsonResponse({"filter_list": filter_list, "clothes_list": clothes_lists}, status = 200)

        except KeyError:
            return JsonResponse({"message":"INVALID_KEYS"}, status = 400)

    def post(self, request, gender, clothes_type):
        filter_data = json.loads(request.body)

        req_color = filter_data.get('color', None)
        req_size  = filter_data.get('size', None)
        req_price = filter_data.get('price', 0)

        try:
            clothes_list = ClothesImage.objects.select_related('clothes').filter(
                clothes__main_category_id = gender,
                clothes__sub_category_id  = clothes_type,
            )

            if req_color:
                clothes_list = clothes_list.filter(color_id = req_color)
            if req_size:
                clothes_list = clothes_list.filter(clothes__clothessize__size_id = req_size)
            if req_price:
                clothes_list = clothes_list.filter(clothes__price__lte = req_price)

            clothes_lists = [
                {
                    'id '          : result.clothes_id,
                    'image'        : result.image1,
                    'color'        : result.color_id,
                    'new'          : result.clothes.is_new,
                    'name'         : result.clothes.name,
                    'price'        : result.clothes.price,
                    'other_colors' : len(clothes_list.filter(clothes_id = result.clothes_id))-1
                } for result in clothes_list]

            if len(clothes_lists) == 0:
                return JsonResponse({"message": "ITEM_DOES_NOT_EXIST"}, status = 400)

            return JsonResponse({"clothes_list": clothes_lists}, status = 200)

        except KeyError:
            return JsonResponse({"message": "INVALID_KEYS"}, status = 400)

class ClothesNewView(View):
    def get(self, request, gender):
        try:
            clothes_list = ClothesImage.objects.select_related('clothes').filter(
                clothes__main_category_id = gender,
                clothes__is_new           = True
             ).order_by('clothes__price')

            deduplication_color = sorted(set([(clothes.color.id, clothes.color.name) for clothes in clothes_list]))

            size_list          = Size.objects.prefetch_related('clothes_set').filter(clothes__main_category_id = gender)
            deduplication_size = sorted(set([(size.id, size.name) for size in size_list]))

            price_list = [price for price in range(round(clothes_list[0].clothes.price + 5000, -4),
                                                   round(clothes_list[len(clothes_list)-1].clothes.price + 35000, -4), 30000)]

            filter_list = {
                'colors' : extract_data("colors", deduplication_color),
                'sizes'  : extract_data("sizes", deduplication_size),
                'prices' : [{"id": index, "name": value} for index, value in enumerate(price_list)]
            }

            clothes_new    = New.objects.select_related('main_category').filter(main_category_id = gender)
            marketing_list = list(clothes_new.values_list('image', flat = True))

            new_list = [
                {
                    'id'           : result.clothes_id,
                    'image'        : result.image1,
                    'color'        : result.color_id,
                    'new'          : result.clothes.is_new,
                    'name'         : result.clothes.name,
                    'price'        : result.clothes.price,
                    'other_colors' : len(clothes_list.filter(clothes_id = result.clothes_id))-1
                } for result in clothes_list]

            return JsonResponse({"filter_list": filter_list, "marketing": marketing_list, "new": new_list}, status = 200)

        except KeyError:
            return JsonResponse({"message":"INVALID_KEYS"}, status = 400)

class ClothesDetailView(View):
    def get(self, request, req_clothes_id, req_color_id):
        try:
            if not ClothesImage.objects.filter(clothes_id = req_clothes_id, color_id = req_color_id).exists():
                return HttpResponse(status = 404)

            clothes_detail = Clothes.objects.prefetch_related('clothesimage_set',
                                                              'clothescare_set',
                                                              'clothessize_set').get(id = req_clothes_id)

            color_name   = Color.objects.get(id = req_color_id).name
            clothes_name = Clothes.objects.get(id = req_clothes_id).name

            composition = clothes_detail.composition.split("}, ")
            for index, value in enumerate(composition[:-1]):
                composition[index] = value + "}"

            clothes_details = {
                'images'       : list(list(clothes_detail.clothesimage_set.filter(color_id = req_color_id).values(
                    'main_image', 'image1', 'image2', 'image3', 'image4', 'image5', 'image6', 'image7'))[0].values()),
                'clothes'      : {"id" : req_clothes_id, "name" : clothes_name},
                'price'        : clothes_detail.price,
                'color'        : {"id" : req_color_id, "name" : color_name},
                'description'  : clothes_detail.description,
                'size'         : [{"id" : element["size_id"], "name" : element["size__name"]}
                                  for element in list(clothes_detail.clothessize_set.values('size_id', 'size__name'))],
                'other_colors' : [{"id" : element["color_id"], "name" : element["color__name"], "image" : element["image1"]}
                                  for element in list(clothes_detail.clothesimage_set.values('color_id', 'color__name', 'image1'))],
                'composition'  : [literal_eval(element) for element in composition],
                'care'         : list(clothes_detail.clothescare_set.values_list('care__name', flat = True))
            }

            for color in clothes_details["other_colors"]:
                if color["name"] == clothes_details["color"]["name"]:
                    clothes_details["other_colors"].remove(color)
                    break

            return JsonResponse({"clothes_details": clothes_details}, status = 200)

        except KeyError:
            return JsonResponse({"message": "INVALID_KEYS"}, status = 400)

class SearchView(View):
    def get(self, request):
        try:
            keyword = request.GET.get('keyword', None)

            clothes_list = ClothesImage.objects.select_related('clothes').filter(clothes__name__icontains = keyword)

            name_list = [element.clothes.name for element in clothes_list]
            if len(name_list) < 5:
                search_list = random.sample(name_list, len(name_list))
            else:
                search_list = random.sample(name_list, 5)

            result_list = [
                {
                    'id'           : result.clothes_id,
                    'image'        : result.image1,
                    'color'        : result.color_id,
                    'new'          : result.clothes.is_new,
                    'name'         : result.clothes.name,
                    'price'        : result.clothes.price,
                    'other_colors' : len(clothes_list.filter(clothes_id = result.clothes_id))-1
                } for result in clothes_list]

            if len(result_list) == 0:
                return JsonResponse({"message": "ITEM_DOES_NOT_EXIST"}, status = 400)

            return JsonResponse({"list" : search_list, "results": result_list}, status = 200)

        except KeyError:
            return JsonResponse({"message": "INVALID_KEYS"}, status = 400)
