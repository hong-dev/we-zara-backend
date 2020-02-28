from  .views import ShowMap

from django.urls import path, include

urlpatterns = [
    path('', ShowMap.as_view()),
    
]
