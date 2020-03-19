from .views import CartView

from django.urls import path,include

urlpatterns = [
    path('', CartView.as_view())
]

