from rest_framework import serializers
from .models import Listing


class ListingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Listing
        fields = (
            "realtor",
            "title",
            "slug",
            "address",
            "city",
            "state",
            "zipcode",
            "description",
            "price",
            "bedrooms",
            "bathroom",
            "sale_type",
            "home_type",
            "main_photo",
            "photo_1",
            "photo_2",
            "photo_3",
            "is_puplished",
            "date_created",
        )
