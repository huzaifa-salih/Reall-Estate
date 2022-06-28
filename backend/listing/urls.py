from django.urls import path
from .views import ManageListingview


urlpatterns = [
    path('manage/', ManageListingview.as_view()),

]