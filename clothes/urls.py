from .views import (
    SubCategoryView,
    ClothesDetailView,
    ClothesNewView,
    SearchView
)

from django.urls import path

urlpatterns = [
    path('/details/<slug:req_clothes_id>/<slug:req_color_id>', ClothesDetailView.as_view()),
    path('/new/<slug:gender>', ClothesNewView.as_view()),
    path('/search', SearchView.as_view()),
    path('/<slug:gender>/<slug:clothes_type>', SubCategoryView.as_view()),
]
