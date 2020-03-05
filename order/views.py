import json

from .models import  Order,OrderedClothes,OrderStatus

from account.models import Account
from account.utils   import login_required

from django.db.models import ExpressionWrapper, F, Count, Aggregate, DecimalField,Sum
from django.views import View
from django.http  import HttpResponse, JsonResponse
from django.core.exceptions import ObjectDoesNotExist,ValidationError,FieldDoesNotExist


class CartView(View):
    @login_required
    def get(self, request):
        try:
            user_data    = request.user.email
            user_id      = Account.objects.get(email = user_data).id
            get_order    = Order.objects.filter(account = user_id).get()
            order        = get_order.orderedclothes_set.all().annotate(a_price=ExpressionWrapper(F('quantity')*F('clothes__price'),output_field=DecimalField(10,2)))
            clothes_list =[
                {
                    'ordered_clothes_id'   :result.id,
                    'clothes_name'         :result.clothes.name,
                    'color_name'           :result.color.name,
                    'size_name'            :result.size.name,
                    'main_image'           :result.clothes.clothesimage_set.get().image1,
                    'quantity'             :result.quantity,
                    'price'                :result.a_price
                }
            for result in order]
            clothes_list.append(order.aggregate(Sum('a_price')))
            clothes_list.append({"order_id":get_order.id})
            return JsonResponse({"message":clothes_list},status=200)

        except ObjectDoesNotExist:
            return HttpResponse(status=400)
        except ValidationError:
            return HttpResponse(status=400)
        except FieldDoesNotExist:
            return HttpResponse(status=400)
        except KeyError:
            return HttpResponse(status=400)
            
    @login_required
    def post(self, request):
        try:
            data      = json.loads(request.body)
            user_data = request.user.email
            user_id   = Account.objects.get(email=user_data).id
            order     = Order.objects.filter(account=user_id)
            if order.exists():
                orderclothes=OrderedClothes.objects.filter(
                    order   = order.get().id,
                    clothes = data['clothes_id'],
                    size    = data['size_id'],
                    color   = data['color_id']
                )
                if orderclothes.exists():
                    orderclothes.update(quantity=orderclothes.get().quantity +1)
                else:
                    OrderedClothes.objects.create(
                        order_id   = order.get().id,
                        clothes_id = data['clothes_id'],
                        size_id    = data['size_id'],
                        color_id   = data['color_id'],
                        quantity   = 1
                    )
            else:
                order=Order.objects.create(
                    account_id      = user_id,
                    order_status_id = 1
                )
                # order.update()
                OrderedClothes.objects.create(
                    order_id   = order.id,
                    clothes_id = data['clothes_id'],
                    size_id    = data['size_id'],
                    color_id   = data['color_id'],
                    quantity   = 1
                )
            return HttpResponse(status=200)

        except ObjectDoesNotExist:
            return HttpResponse(status=400)
        except ValidationError:
            return HttpResponse(status=400)
        except FieldDoesNotExist:
            return HttpResponse(status=400)
        except KeyError:
            return HttpResponse(status=400)

    @login_required
    def delete(self, request):
        try:
            data                   = json.loads(request.body)
            get_ordered_clothes_id = data['ordered_clothes_id']
            get_order_id           = data['order_id']
            order                  = Order.objects.filter(id=get_order_id)
            orderclothes           = order.get().orderedclothes_set.filter(id=get_ordered_clothes_id)

            if orderclothes.exists()  and Order.objects.filter(id=get_order_id).exists():
                clothes_quantity = orderclothes.get().quantity
                print(clothes_quantity)
                if  clothes_quantity > 1:
                    orderclothes.update(quantity=clothes_quantity-1)
                else :
                    orderclothes.get().delete()
                    if not(orderclothes.exists()):
                        order.delete()
                return HttpResponse(status=200)

        except ObjectDoesNotExist:
            return HttpResponse(status=400)
        except ValidationError:
            return HttpResponse(status=400)
        except FieldDoesNotExist:
            return HttpResponse(status=400)
        except KeyError:
            return HttpResponse(status=400)
