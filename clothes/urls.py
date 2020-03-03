from .views import SubCategoryView

from django.urls import path

urlpatterns = [
    path('/<slug:gender>/<slug:clothes_type>', SubCategoryView.as_view()),
]
