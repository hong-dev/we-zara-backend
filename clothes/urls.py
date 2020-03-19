from .views import (
    SubCategoryView,
    ClothesDetailView,
    ClothesNewView,
    SearchView
)

from django.urls import path

urlpatterns = [
    path('/<int:clothes_id>', ClothesDetailView.as_view()),
    path('/new/<int:gender_id>', ClothesNewView.as_view()),
    path('', SearchView.as_view()),
    #path('/<int:gender_id>/<int:clothes_type>', SubCategoryView.as_view()),
]
