from .views import ClothesDetailView

from django.urls import path

urlpatterns = [
    path('/details/<slug:req_clothes_id>/<slug:req_color_id>', ClothesDetailView.as_view()),
]
