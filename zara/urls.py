from django.urls import path, include

urlpatterns = [
    path('account', include('account.urls')),
    path('store-info',include('store.urls'))
]
