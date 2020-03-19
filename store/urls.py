from  .views import ShowMap
from django.urls import path

urlpatterns = [
    path('', MapView.as_view()), 
]
