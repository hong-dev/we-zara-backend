import json
import collections

from .models import Clothes, Color, Size, ClothesImage, New

from django.views import View
from django.http  import HttpResponse, JsonResponse

def extract_data(field_name, deduplicated_list):
    field_spec      = collections.namedtuple(field_name, f"{field_name}_id, {field_name}_name")
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

            deduplication_color = set([(clothes.color.id, clothes.color.name) for clothes in clothes_list])

            size_list          = Size.objects.prefetch_related('clothes_set').filter(clothes__main_category_id = gender, clothes__sub_category_id = clothes_type)
            deduplication_size = set([(size.id, size.name) for size in size_list])

            filter_list = {
                'colors' : extract_data("colors", deduplication_color),
                'sizes'  : extract_data("sizes", deduplication_size),
                'prices' : {"min_price" : clothes_list[0].clothes.price,
                            "max_price" : clothes_list[len(clothes_list)-1].clothes.price}
            }

            clothes_lists = [
                {
                    'id '          : result.clothes.id,
                    'image'        : result.main_image,
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
                    'image'        : result.main_image,
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

            deduplication_color = set([(clothes.color.id, clothes.color.name) for clothes in clothes_list])

            size_list          = Size.objects.prefetch_related('clothes_set').filter(clothes__main_category_id = gender)
            deduplication_size = set([(size.id, size.name) for size in size_list])

            filter_list = {
                'colors' : extract_data("colors", deduplication_color),
                'sizes'  : extract_data("sizes", deduplication_size),
                'prices' : {"min_price" : clothes_list[0].clothes.price,
                            "max_price" : clothes_list[len(clothes_list)-1].clothes.price}
            }

            clothes_new    = New.objects.select_related('main_category').filter(main_category_id = gender)
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

            return JsonResponse({"filter_list": filter_list, "marketing": marketing_list, "new": new_list}, status = 200)

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

            search_list = [element.clothes.name for element in clothes_list][:5]

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
