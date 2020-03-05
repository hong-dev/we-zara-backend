from .views import (
    SubCategoryView,
    ClothesDetailView,
    ClothesNewView,
    SearchView
)

from django.urls import path

urlpatterns = [
    path('/details/<int:req_clothes_id>/<int:req_color_id>', ClothesDetailView.as_view()),
    path('/new/<int:gender>', ClothesNewView.as_view()),
    path('/search', SearchView.as_view()),
    path('/<int:gender>/<int:clothes_type>', SubCategoryView.as_view()),
]
