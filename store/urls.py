from  .views import ShowMap
from django.urls import path

urlpatterns = [
    path('', ShowMap.as_view()), 
]
