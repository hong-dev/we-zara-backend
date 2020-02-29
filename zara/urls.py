from django.urls import path, include

urlpatterns = [
    path('account', include('account.urls')),
    path('clothes', include('clothes.urls')),
]
