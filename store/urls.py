from  .views import ShowMap

from django.urls import path, include

urlpatterns = [
    path('/map-data', ShowMap.as_view()),
]
