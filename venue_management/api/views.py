from django.shortcuts import render
# Create your views here.



from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import SearchFilter
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser

from ..models import Venue, Amenities, VenueImage
from .serializer import VenueListSerializer, VenueSerializer, AmenitiesSerializer, VenueImageSerializer
from rest_framework.permissions import IsAuthenticated

class VenueListView(ListAPIView):
    permission_classes = []
    queryset = Venue.objects.order_by('created_at')
    pagination_class = PageNumberPagination
    filter_backends = [SearchFilter]
    search_fields = ['name', 'full_address', 'venue_type', 'management_company', 'reservation_status']
    serializer_class = VenueListSerializer

    def list(self, request, *args, **kwargs):
        self.pagination_class.page_size = 4
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            total_pages = self.paginator.page.paginator.num_pages if self.paginator else 1
            current_page = self.paginator.page.number if self.paginator else 1

            data = {
                'total_pages': total_pages,
                'current_page': current_page,
                'results': serializer.data
            }
            return self.get_paginated_response(data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)



class VenueRetrieveAPIView(RetrieveAPIView):
    queryset = Venue.objects.all()
    serializer_class = VenueSerializer
    permission_classes = []
    

    

class VenueImageListAPIView(ListAPIView):
    serializer_class = VenueImageSerializer
    permission_classes = []
    parser_classes = [MultiPartParser]

    def get_queryset(self):
        venue_id = self.request.query_params.get('venueId')  # Use query_params for GET request
        if venue_id:
            queryset = VenueImage.objects.filter(venue_id=venue_id)
        else:
            queryset = VenueImage.objects.none()  # Return an empty queryset if no venueId is provided
        return queryset