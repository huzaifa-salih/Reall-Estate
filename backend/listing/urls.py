from django.urls import path
from .views import ManageListingview, ListingDetailView, ListingView, SearchListingView


urlpatterns = [
    path("manage/", ManageListingview.as_view()),
    path("detail/", ListingDetailView.as_view()),
    path("get-listings/", ListingView.as_view()),
    path("search/", SearchListingView.as_view()),
]
