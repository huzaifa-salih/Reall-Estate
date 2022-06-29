from django.urls import path
from .views import ManageListingview, ListingDetailView, ListingView


urlpatterns = [
    path("manage/", ManageListingview.as_view()),
    path("detail/", ListingDetailView.as_view()),
    path("get-listings/", ListingView.as_view()),

]
