from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from .models import Listing
from .serializer import ListingSerializer
from django.contrib.postgres.search import SearchVector, SearchQuery


class ManageListingview(APIView):
    def get(self, request, format=None):
        try:
            user = request.user
            if not user.is_realtor:
                return Response({"error": "User does not have necessary permissions for getting this listing data"}, status=status.HTTP_403_FORBIDDEN)

            slug = request.query_params.get("slug")
            if not slug:
                listing = Listing.objects.order_by("-date_created").filter(realtor=user.email)
                listing = ListingSerializer(listing, many=True)
                return Response({"listings": listing.data}, status=status.HTTP_200_OK)
            if not Listing.objects.filter(realtor=user.email, slug=slug).exists():
                return Response({"error": "Listing not found"}, status=status.HTTP_404_NOT_FOUND)
            listing = Listing.objects.get(realtor=user.email, slug=slug)
            listing = ListingSerializer(listing)
            return Response({"listing": listing.data}, status=status.HTTP_200_OK)

        except:
            return Response({"error": "Something went wrong when retrieving listing or listing detail"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def retrieve_values(self, data):
        title = data["title"]
        slug = data["slug"]
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

        data = {
            "title": title,
            "slug": slug,
            "address": address,
            "city": city,
            "state": state,
            "zipcode": zipcode,
            "description": description,
            "price": price,
            "bedrooms": bedrooms,
            "bathroom": bathroom,
            "sale_type": sale_type,
            "home_type": home_type,
            "main_photo": main_photo,
            "photo_1": photo_1,
            "photo_2": photo_2,
            "photo_3": photo_3,
            "is_puplished": is_puplished,
        }

    def post(self, request):
        try:
            user = request.user
            if not user.is_realtor:
                return Response({"error": "User does not have necessary permissions for creating this listing data"}, status=status.HTTP_403_FORBIDDEN)

            data = request.data
            data = self.retrieve_values(data)

            if data == -1:
                return Response({"error": "Price must be an integer"}, status=status.HTTP_400_BAD_REQUEST)
            elif data == -2:
                return Response({"error": "Bedrooms must be an integer"}, status=status.HTTP_400_BAD_REQUEST)
            elif data == -3:
                return Response({"error": "Bathrooms must be a floating point value"}, status=status.HTTP_400_BAD_REQUEST)

            title = data["title"]
            slug = data["slug"]
            address = data["address"]
            city = data["city"]
            state = data["state"]
            zipcode = data["zipcode"]
            description = data["description"]
            price = data["price"]
            bedrooms = data["bedrooms"]
            bathroom = data["bathroom"]
            sale_type = data["sale_type"]
            home_type = data["home_type"]
            main_photo = data["main_photo"]
            photo_1 = data["photo_1"]
            photo_2 = data["photo_2"]
            photo_3 = data["photo_3"]
            is_published = data["is_published"]

            if Listing.objects.filter(slug=slug).exists():
                return Response({"error": "Listing with this slug already exists"}, status=status.HTTP_400_BAD_REQUEST)

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
                is_published=is_published,
            )
            return Response({"success": "Listing created successfully"}, status=status.HTTP_201_CREATED)
        except:
            return Response({"error": "Something went wrong when creating listing"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, format=None):
        try:
            user = request.user
            if not user.is_realtor:
                return Response({"error": "user dose not have necessary permission for updating this listing data."}, status=status.HTTP_403_FORBIDDEN)

            data = request.data
            data = self.retrieve_values(data)
            title = data["title"]
            slug = data["slug"]
            address = data["address"]
            city = data["city"]
            state = data["state"]
            zipcode = data["zipcode"]
            description = data["description"]
            price = data["price"]
            bedrooms = data["bedrooms"]
            bathroom = data["bathroom"]
            sale_type = data["sale_type"]
            home_type = data["home_type"]
            main_photo = data["main_photo"]
            photo_1 = data["photo_1"]
            photo_2 = data["photo_2"]
            photo_3 = data["photo_3"]
            is_puplished = data["is_puplished"]

            if not Listing.objects.filter(realtor=user.email, slug=slug).exists():
                return Response({"error": "Listings dose not exist."}, status=status.HTTP_404_NOT_FOUND)

            Listing.objects.filter(realtor=user.email, slug=slug).update(
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
            return Response({"success": "listing updated successfully."}, status=status.HTTP_200_OK)
        except:
            return Response({"error": "Something went wrong when updating listing"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def patch(self, request):
        try:
            user = request.user
            if not user.is_realtor:
                return Response({"error": "user dose not have necessary permission for updating this listing data."}, status=status.HTTP_403_FORBIDDEN)

            data = request.data
            slug = data["slug"]
            is_published = data["is_published"]
            if is_published == "True":
                is_published = True
            else:
                is_published = False

            if not Listing.objects.filter(realtor=user.email, slug=slug).exists():
                return Response({"error": "Listings dose not exist."}, status=status.HTTP_404_NOT_FOUND)

            Listing.objects.filter(realtor=user.email, slug=slug).update(is_published=True)
            return Response({"success": "Listings published status updated successfully"}, status=status.HTTP_200_OK)
        except:
            return Response({"error": "Something went wrong when retrieving listing"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request):
        try:
            user = request.user
            if not user.is_realtor:
                return Response({"error": "user dose not have necessary permission for deleting this listing data."}, status=status.HTTP_403_FORBIDDEN)

            data = request.data
            slug = data["slug"]
            if not Listing.objects.filter(realtor=user.email, slug=slug).exists():
                return Response({"error": "Listings you are trying to delete dose not exist."}, status=status.HTTP_404_NOT_FOUND)

            Listing.objects.filter(realtor=user.email, slug=slug).delete()
            if not Listing.objects.filter(realtor=user.email, slug=slug).exists():
                return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({"error": "Faield to delete listing"}, status=status.HTTP_400_BAD_REQUEST)

        except:
            return Response({"error": "Something went wrong when retrieving listing"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ListingDetailView(APIView):
    def get(self, request, format=None):
        try:
            slug = request.query_params.get("slug")
            if not slug:
                return Response({"error": "Must provid a slug"}, status=status.HTTP_400_BAD_REQUEST)
            if not Listing.objects.filter(slug=slug, is_published=True).exists():
                return Response({"error": "Published listing with this slug dos not exists"}, status=status.HTTP_404_NOT_FOUND)
            listing = Listing.objects.get(slug=slug, is_published=True)
            listing = ListingSerializer(listing)
            return Response({"listing": listing.data}, status=status.HTTP_200_OK)

        except:
            return Response({"error": "Error Retrieving listing"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ListingView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, format=None):
        try:
            slug = request.query_params.get("slug")
            if not Listing.objects.filter(slug=slug, is_published=True).exists():
                return Response({"error": "No Published listings in the database"}, status=status.HTTP_404_NOT_FOUND)
            listings = Listing.objects.order_by("-date_created").filter(is_published=True)
            listings = ListingSerializer(listings, many=True)
            return Response({"listings": listings.data}, status=status.HTTP_200_OK)

        except:
            return Response({"error": "Somthing went wrong when Retrieving listing"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SearchListingView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, format=None):
        try:
            city = request.query_params.get("city")
            state = request.query_params.get("state")
            max_price = request.query_params.get("max_price")
            try:
                max_price = int(max_price)
            except:
                return Response({"error": "Max Price must be an integer"}, status=status.HTTP_400_BAD_REQUEST)

            bedrooms = request.query_params.get("bedrooms")
            try:
                bedrooms = int(bedrooms)
            except:
                return Response({"error": "bedrooms must be an integer"}, status=status.HTTP_400_BAD_REQUEST)

            bathroom = request.query_params.get("bathroom")
            try:
                bathroom = float(bathroom)
            except:
                return Response({"error": "bathrooms must be a floting point value"}, status=status.HTTP_400_BAD_REQUEST)
            if bathroom <= 0 or bathroom >= 10:
                bathroom = 1.0
            bathroom = round(bathroom, 1)

            sale_type = request.query_params.get("sale_type")
            if sale_type == "FOR_SALE":
                sale_type = "For Sale"
            else:
                sale_type = "For Rant"

            home_type = request.query_params.get("home_type")
            if home_type == "HOUSE":
                home_type = "House"
            elif home_type == "CONDO":
                home_type = "Condo"
            else:
                home_type = "TownHouse"

            search = request.query_params.get("search")
            if not search:
                return Response({"error": "Must pass search criteria"}, status=status.HTTP_400_BAD_REQUEST)

            vector = SearchVector("title", "description")
            query = SearchQuery(search)
            if (
                not Listing.objects.annotate(search=vector)
                .filter(
                    search=query,
                    city=city,
                    state=state,
                    price__lte=max_price,
                    bedrooms__gte=bedrooms,
                    bathroom__gte=bathroom,
                    sale_type=sale_type,
                    home_type=home_type,
                    is_published=True,
                )
                .exists()
            ):
                return Response({"error": "Not listing found with this criteria."}, status=status.HTTP_404_NOT_FOUND)

            listings = Listing.objects.annotate(search=vector).filter(
                search=query,
                city=city,
                state=state,
                price__lte=max_price,
                bedrooms__gte=bedrooms,
                bathroom__gte=bathroom,
                sale_type=sale_type,
                home_type=home_type,
                is_published=True,
            )
            listings = ListingSerializer(listings, many=True)
            return Response({"listings": listings.data}, status=status.HTTP_200_OK)

        except:
            return Response({"error": "Somthing went wrong when Searching listing"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
