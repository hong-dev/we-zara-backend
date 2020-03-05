from .views import CartView

from django.urls import path,include

urlpatterns = [
    path(('/cart'),CartView.as_view())
]

