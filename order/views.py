import json

from .models import Order,OrderedClothes,OrderStatus

from account.models import Account
from account.utils  import login_required

from django.db.models       import ExpressionWrapper, F, Count, Aggregate, DecimalField,Sum
from django.views           import View
from django.http            import HttpResponse, JsonResponse
from django.core.exceptions import ObjectDoesNotExist,ValidationError,FieldDoesNotExist


class CartView(View):
    NEW = 1

    @login_required
    def get(self, request):
        try:
            user_order   = Order.objects.filter(account = request.user).get()
            order        = (
                user_order
                .orderedclothes_set.all()
                .annotate(
                    a_price=ExpressionWrapper(F('quantity')*F('clothes__price'),
                    output_field=DecimalField(10,2))
                )
            )

            clothes_list =[
                {
                    'ordered_clothes_id'   :result.id,
                    'clothes_name'         :result.clothes.name,
                    'color_name'           :result.color.name,
                    'size_name'            :result.size.name,
                    'main_image'           :result.clothes.clothesimage_set.get().image1,
                    'quantity'             :result.quantity,
                    'price'                :result.a_price
                } for result in order
            ]
            result             = {"clothes_list" : clothese_list}
            result['a_price']  = order.aggregate(Sum('a_price'))
            result['order_id'] = user_order.id

            return JsonResponse(result, status=200)
        except Order.DoesNotExist:
            return HttpResponse(status=400)
        except KeyError:
            return HttpResponse(status=400)

    @login_required
    def post(self, request):
        try:
            data  = json.loads(request.body)
            order = Order.objects.get_or_create(
                account_id      = request.user,
                order_status_id = self.NEW
            )
            
            clothese = orderedclothes_set.update_or_create(
                clothes = data['clothes_id'],
                size    = data['size_id'],
                color   = data['color_id'].
                default = {quantity: quantity + 1}
            )

            return HttpResponse(status=200)
        except Order.DoesNotExist:
            return HttpResponse(status=400)
        except KeyError:
            return HttpResponse(status=400)

    @login_required
    def delete(self, request):
        try:
			data       = json.loads(request.body)
			clothes_id = data['ordered_clothes_id']
			order_id   = data['ordered__id']

			with transaction() as tran:
				orderclothes = OrderClothes.filter(id  = get_ordered_clothes_id)
				order        = Order.objects.filter(id = get_order_id) # <==

				clothes_quantity = orderclothes.get().quantity
				order_clothes.delete()
				order.update(quantity=clothes_quantity-1)

				return HttpResponse(status=200)
        except ObjectDoesNotExist:
            return HttpResponse(status=400)
        except KeyError:
            return HttpResponse(status=400)
