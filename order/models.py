import uuid
import json
import bcrypt
import requests

from django.db import models
from account.models import Account
from clothes.models import Clothes,Size,Color
from account.utils import login_required

class Order(models.Model):
    order_number  = models.UUIDField(default= uuid.uuid4, editable=False, unique=True)
    account       = models.ForeignKey(Account, on_delete = models.SET_NULL, null = True)
    order_status  = models.ForeignKey('OrderStatus', on_delete = models.SET_NULL, null = True)
    created_at    = models.DateTimeField(auto_now_add = True)
    updated_at    = models.DateTimeField(auto_now = True)
    class Meta:
        db_table ='orders'

class OrderedClothes(models.Model):
    order    = models.ForeignKey(Order, on_delete = models.SET_NULL, null = True)
    clothes  = models.ForeignKey(Clothes, on_delete = models.SET_NULL, null = True)
    size     = models.ForeignKey(Size, on_delete    = models.SET_NULL, null = True)
    color    = models.ForeignKey(Color, on_delete   = models.SET_NULL, null = True)
    quantity = models.IntegerField(default = 0)
    class Meta:
        db_table ='ordered_clothes'

class OrderStatus(models.Model):
    name = models.CharField(max_length=45)
    class Meta:
        db_table ='order_status'

