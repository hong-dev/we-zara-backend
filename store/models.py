from django.db import models

# Create your models here.


class Store (models.Model):
    name      = models.CharField(max_length=50)
    address   = models.CharField(max_length=100)
    longitude = models.DecimalField(max_digits=8, decimal_places=5)
    latitude  = models.DecimalField(max_digits=8, decimal_places=5)

    class Meta:
        db_table = 'stores'




