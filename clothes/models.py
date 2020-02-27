from django.db import models

class MainCategory(models.Model):
    gender = models.CharField(max_length = 20)

    class Meta:
        db_table = 'main_categories'

class SubCategory(models.Model):
    clothes_type  = models.CharField(max_length = 45)
    main_category = models.ForeignKey(MainCategory, on_delete = models.SET_NULL, null = True)

    class Meta:
        db_table = 'sub_categories'

class ItemCategory(models.Model):
    item_type     = models.CharField(max_length = 45)
    main_category = models.ForeignKey(MainCategory, on_delete = models.SET_NULL, null = True)
    sub_category  = models.ForeignKey(SubCategory, on_delete = models.SET_NULL, null = True)

    class Meta:
        db_table = 'item_categories'

class Clothes(models.Model):
    name          = models.CharField(max_length = 45)
    main_category = models.ForeignKey(MainCategory, on_delete = models.SET_NULL, null = True)
    sub_category  = models.ForeignKey(SubCategory, on_delete = models.SET_NULL, null = True)
    item_category = models.ForeignKey(ItemCategory, on_delete = models.SET_NULL, null = True)
    price         = models.DecimalField(max_digits = 8, decimal_places = 5)
    description   = models.TextField
    composition   = models.TextField
    bestseller    = models.BooleanField
    size          = models.ManyToManyField('Size', through = 'ClothesSize')
    color         = models.ManyToManyField('Color', through = 'ClothesColor')
    care          = models.ManyToManyField('Care', through = 'ClothesCare')
    created_at    = models.DateTimeField(auto_now_add = True)
    updated_at    = models.DateTimeField(auto_now = True)

    class Meta:
        db_table = 'clothes'

class ClothesImage(models.Model):
    clothes = models.ForeignKey('Clothes', on_delete = models.SET_NULL, null = True)
    color   = models.ForeignKey('Color', on_delete = models.SET_NULL, null = True)
    image   = models.URLField(max_length = 500)

    class Meta:
        db_table = 'clothes_image'

class Size(models.Model):
    name = models.CharField(max_length = 20)

    class Meta:
        db_table = 'sizes'

class ClothesSize(models.Model):
    clothes = models.ForeignKey('Clothes', on_delete = models.SET_NULL, null = True)
    size    = models.ForeignKey('Size', on_delete = models.SET_NULL, null = True)

    class Meta:
        db_table = 'clothes_sizes'

class Color(models.Model):
    name = models.CharField(max_length = 20)

    class Meta:
        db_table = 'colors'

class ClothesColor(models.Model):
    clothes = models.ForeignKey('Clothes', on_delete = models.SET_NULL, null = True)
    color   = models.ForeignKey('Color', on_delete = models.SET_NULL, null = True)

    class Meta:
        db_table = 'clothes_colors'

class Care(models.Model):
    name = models.TextField

    class Meta:
        db_table = 'cares'

class ClothesCare(models.Model):
    clothes = models.ForeignKey('Clothes', on_delete = models.SET_NULL, null = True)
    care    = models.ForeignKey('Care', on_delete = models.SET_NULL, null = True)

    class Meta:
        db_table = 'clothes_cares'
