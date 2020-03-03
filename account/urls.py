from .views import SignupView, SigninView, AccountView

from django.urls import path

urlpatterns = [
    path('/sign-up', SignupView.as_view()),
    path('/sign-in', SigninView.as_view()),
]
