from rest_framework.views import APIView
from rest_framework.filters import SearchFilter
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveUpdateAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .permissions import IsAuthAdmin
from rest_framework.exceptions import AuthenticationFailed,ParseError
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status


from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate
from django.http import Http404
from decouple import config
from django.conf import settings
from accounts.models import Account, ClientProfile
from venue_management.models import Venue, Amenities, VenueImage
from .serializer import ClientSerializer, VenueListSerializer, VenueSerializer, AmenitiesSerializer
from django.contrib.auth import get_user_model
import json
# Create your views here.
User = get_user_model()



class LoginView(APIView):

    def post(self,request):
        try:
            email = request.data['email']
            password = request.data['password']
        except KeyError:
            raise ParseError('All Fields Are Required')
        
        try:
            user = Account.objects.get(email = email)
        except Exception as e:
            raise AuthenticationFailed('Invalid Email Address')
        
        if not user.is_superadmin:
            raise AuthenticationFailed("You don't have permission to page.")
        
        user = authenticate(username=email, password=password)
        if user is None:
            raise AuthenticationFailed('Invalid Password')
        if user.user_role != 'ADMIN':
            raise AuthenticationFailed("You don't have permission to enter this page.")

        refresh = RefreshToken.for_user(user)
        refresh["username"] = str(user.username)
        refresh['user_role'] = str(user.user_role)
        # refresh['profile_image'] = ""
        content = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            }
        
        return Response(content, status=status.HTTP_200_OK)


class AdminClientUserListCreateView(ListAPIView):
    permission_classes = [IsAuthAdmin]
    queryset = ClientProfile.objects.filter(client__user_role = 'CLIENT').order_by('client__date_joined')
    serializer_class = ClientSerializer
    pagination_class = PageNumberPagination
    filter_backends = [SearchFilter]
    search_fields = ['first_name', 'last_name', 'area_of_preference']

    def list(self, request, *args, **kwargs):
        self.pagination_class.page_size = 2
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)
        total_pages = self.paginator.page.paginator.num_pages if self.paginator else 1
        current_page = self.paginator.page.number if self.paginator else 1
        
        # Prepare the response data including pagination metadata
        data = {
            'total_pages': total_pages,
            'current_page': current_page,
            'results': serializer.data
        }
        
        # Return the paginated response
        return self.get_paginated_response(data)

class ClientRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    queryset = ClientProfile.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [IsAuthAdmin]


# ====Venue Management start====




class AdminVenueListCreateView(ListCreateAPIView):
    permission_classes = [IsAuthAdmin]
    queryset = Venue.objects.order_by('created_at')
    pagination_class = PageNumberPagination
    filter_backends = [SearchFilter]
    search_fields = ['name', 'full_address', 'venue_type', 'management_company', 'reservation_status']

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return VenueListSerializer
        elif self.request.method == 'POST':
            return VenueSerializer

    def list(self, request, *args, **kwargs):
        self.pagination_class.page_size = 4
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)
        total_pages = self.paginator.page.paginator.num_pages if self.paginator else 1
        current_page = self.paginator.page.number if self.paginator else 1

        data = {
            'total_pages': total_pages,
            'current_page': current_page,
            'results': serializer.data
        }
        return self.get_paginated_response(data)
    

class VenueRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    queryset = Venue.objects.all()
    serializer_class = VenueSerializer
    permission_classes = [IsAuthAdmin]


    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        # Additional data to add to the response
        # Fetch all amenities
        all_amenities = Amenities.objects.all()
        amenity_serializer = AmenitiesSerializer(all_amenities, many=True)

        choices = {
            'reservation_choices': [i[0] for i in Venue.RESERVATION_CHOICES],
            'venue_type_choices': [i[0] for i in Venue.VENUE_TYPE_CHOICES],
            'all_amenities': amenity_serializer.data
        }
        # Add additional data to the serialized representation
        response_data = serializer.data
        response_data.update(choices)
        return Response(response_data)

    # def update(self, instance, validated_data):
    #     # Check if 'blockorunblock' is in the validated data
    #     if 'blockorunblock' in validated_data:
    #         blockorunblock = validated_data.pop('blockorunblock')
    #         instance.is_active = not blockorunblock  # Toggle the 'is_active' field based on 'blockorunblock'
    #     else:
    #         # Update the instance with the validated data (excluding 'blockorunblock')
    #         instance = super().update(instance, validated_data)
    #     instance.save()
    #     return instance
   