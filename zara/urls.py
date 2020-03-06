from django.urls import path, include

urlpatterns = [
    path('account', include('account.urls')),
    path('store-info', include('store.urls')),
    path('clothes', include('clothes.urls')),
    path('orders', include('order.urls'))
]
