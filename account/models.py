from django.db import models

class Account(models.Model):
    email      = models.EmailField(max_length = 50, unique = True)
    password   = models.CharField(max_length = 500)
    name       = models.CharField(max_length = 30)
    zip_code   = models.CharField(max_length = 10)
    address_1  = models.CharField(max_length = 200)
    address_2  = models.CharField(max_length = 100, null = True)
    country    = models.CharField(max_length = 30)
    phone      = models.CharField(max_length = 15)
    upper_body = models.CharField(max_length = 10, null = True)
    lower_body = models.CharField(max_length = 10, null = True)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    class Meta:
        db_table = 'accounts'
