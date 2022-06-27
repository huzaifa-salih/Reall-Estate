from django.urls import path
from .views import RegisterUser, RetrieveUser


urlpatterns = [
    path("register", RegisterUser.as_view()),
    path("me", RetrieveUser.as_view()),
]
