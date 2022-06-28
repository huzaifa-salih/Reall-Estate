from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Listing
from .serializer import ListingSerializer


class ManageListingview(APIView):
    def get(self, request, format=None):
        try:
            user = request.user
            if not user.is_realtor:
                return Response({"error": "user dose not have necessary permission for creating this listing data."}, status=status.HTTP_403_FORBIDDEN)

            slug = request.query_params.get("slug")
            if not slug:
                listing = Listing.objects.order_by("-date_created").filter(realtor=user.email)
                listing = ListingSerializer(listing, many=True)
                return Response({"listings": listing.data}, status=status.HTTP_200_OK)
            if Listing.objects.filter(realtor=user.email, slug=slug).exists():
                return Response({"error": "Listing not found."}, status=status.HTTP_404_NOT_FOUND)
            listing = Listing.objects.get(realtor=user.email, slug=slug)
            listing = ListingSerializer(listing)

        except:
            return Response({"error": "Somthing went weong when creating listing."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        try:
            user = request.user
            if not user.is_realtor:
                return Response({"error": "user dose not have necessary permission for creating this listing data."}, status=status.HTTP_403_FORBIDDEN)

                data = request.data
                title = data["title"]

                slug = data["slug"]
                if Listing.objects.filter(slug=slug).exists():
                    return Response({"error": "listings with this slug already exixts."}, status=status.HTTP_400_BAD_REQUEST)

                address = data["address"]
                city = data["city"]
                state = data["state"]
                zipcode = data["zipcode"]
                description = data["description"]
                price = data["price"]
                try:
                    price = int(price)
                except:
                    return Response({"error": "Price must be an integer."}, status=status.HTTP_400_BAD_REQUEST)

                bedrooms = data["bedrooms"]
                try:
                    bedrooms = int(bedrooms)
                except:
                    return Response({"error": "Bedrooms must be an integer."}, status=status.HTTP_400_BAD_REQUEST)

                bathroom = data["bathroom"]
                try:
                    bathroom = float(bathroom)
                except:
                    return Response({"error": "Bathroom must be an floating point value"}, status=status.HTTP_400_BAD_REQUEST)

                if bathroom <= 0 or bathroom >= 10:
                    bathroom = 1.0
                bathroom = round(bathroom, 1)

                sale_type = data["sale_type"]
                if sale_type == "FOR_RENT":
                    sale_type = "For Rent"
                else:
                    sale_type = "For Sale"

                home_type = data["home_type"]
                if home_type == "CONDO":
                    home_type = "Condo"
                elif home_type == "TOWNHOUSE":
                    home_type = "TownHouse"
                else:
                    home_type = "House"

                main_photo = data["main_photo"]
                photo_1 = data["photo_1"]
                photo_2 = data["photo_2"]
                photo_3 = data["photo_3"]

                is_puplished = data["is_puplished"]
                if is_puplished == "True":
                    is_puplished = True
                else:
                    is_puplished = False

                Listing.objects.create(
                    realtor=user.email,
                    title=title,
                    slug=slug,
                    address=address,
                    city=city,
                    state=state,
                    zipcode=zipcode,
                    description=description,
                    price=price,
                    bedrooms=bedrooms,
                    bathroom=bathroom,
                    sale_type=sale_type,
                    home_type=home_type,
                    main_photo=main_photo,
                    photo_1=photo_1,
                    photo_2=photo_2,
                    photo_3=photo_3,
                    is_puplished=is_puplished,
                )
                return Response({"success": "listing created successfully."}, status=status.HTTP_201_CREATED)
        except:
            return Response({"error": "Somthing went weong when creating listing."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
