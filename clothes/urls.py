from .views import SubCategoryView, ClothesDetailView

from django.urls import path

urlpatterns = [
    path('/details/<slug:req_clothes_id>/<slug:req_color_id>', ClothesDetailView.as_view()),
    path('/<slug:gender>/<slug:clothes_type>', SubCategoryView.as_view()),
]