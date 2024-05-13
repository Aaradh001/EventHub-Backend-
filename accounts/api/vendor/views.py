from django.shortcuts import render
from django.contrib.auth import authenticate
from django.http import Http404
from decouple import config
from django.conf import settings
from accounts.models import Account, VendorProfile, OtherServices
from services.models import Service
from .serializers import VendorProfileSerializer, OtherServiceSerializer, ProfileImageSerializer, VendorServiceSerializer, ServiceSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import AuthenticationFailed,ParseError
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView, RetrieveAPIView, UpdateAPIView, ListAPIView, RetrieveDestroyAPIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import get_user_model
from .serializers import ProfileDetailsSerialiser
import json

# Create your views here.

User = get_user_model()



class RegisterView(APIView):
    def post(self,request):
        input_data = {}
        for key, value in request.data.items():
            # If the value is a list and has only one element, extract that element
            if isinstance(value, str) and value.startswith('{') and value.endswith('}'):
                input_data[key] = json.loads(value)
            else:
                input_data[key] = value
        serializer = VendorProfileSerializer(data = input_data)

        if serializer.is_valid():
            vendor = serializer.save()
            logo = request.FILES.get('logo')
            if logo:
                vendor.logo = logo
                vendor.save()

        else:
            return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)  

        content ={'Message':'Vendor Registered Successfully'}
        return Response(content,status=status.HTTP_201_CREATED)
  

class VendorProfileUpdateAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return VendorProfile.objects.get(vendor__id = pk)
        except VendorProfile.DoesNotExist:
            raise Http404

    def put(self, request, *args, **kwargs):
        vendor_profile = self.get_object(pk = request.user.id)
        account = vendor_profile.vendor
        unique_fields = [field.name for field in account._meta.fields if field.unique and not field.name =='id']
        for field in unique_fields:
            if request.data['vendor'][field] == getattr(account, field):
                request.data['vendor'].pop(field)
        serializer = VendorProfileSerializer(vendor_profile, data=request.data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class ProfileImageUpdateView(UpdateAPIView):
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)
    queryset = VendorProfile.objects.all()
    serializer_class = ProfileImageSerializer

    def get_object(self):
        # Get the current user
        try:
            return VendorProfile.objects.get(vendor__id=self.request.user.id)
        except VendorProfile.DoesNotExist as e:
            print(e)
            return Response("Profile not found", status=status.HTTP_404_NOT_FOUND)

    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class LoginView(APIView):

    def post(self,request):
        try:
            email = request.data['email'] #NEED TO CHANGE TO GET
            password = request.data['password']
        
        except KeyError:
            raise ParseError('All Fields Are Required')

        if not Account.objects.filter(email=email).exists(): 
            raise AuthenticationFailed('Invalid Email Address')

        if not Account.objects.filter(email=email,is_active=True).exists():
            raise AuthenticationFailed('You are blocked by admin ! Please contact admin')
        
        user = authenticate(username=email, password=password)
        if user is None:
            raise AuthenticationFailed('Invalid Password')
        if user.user_role != 'VENDOR':
            raise AuthenticationFailed("You don't have permission to enter this page.")
        vendor_profile = VendorProfile.objects.filter(vendor = user).first()
        refresh = RefreshToken.for_user(user)
        refresh["username"] = str(user.username) 
        refresh["status"] = bool(user.is_active)
        refresh["isVerified"] = bool(vendor_profile.is_verification_completed)

        content = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'isAdmin': user.is_superadmin
            }
        
        return Response(content, status=status.HTTP_200_OK)


class VendorDetails(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            user = User.objects.get(id=request.user.id)
            profile = VendorProfile.objects.get(vendor = user)
        except (User.DoesNotExist, VendorProfile.DoesNotExist) as e:
            return Response({"error": "User or profile not found."}, status=404)
       
        data = ProfileDetailsSerialiser(profile).data
        try :
            logo = profile.logo
            if logo:
                image_url = request.build_absolute_uri('/')[:-1] + logo.url
                data['logo'] = image_url
            else:
                data['logo'] = ''
        except:
            data['logo'] = ''
            
        content = data
        return Response(content)


class OtherServicesListView(ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = OtherServices.objects.all().order_by('name')
    serializer_class = OtherServiceSerializer

    def perform_create(self, serializer):
        # Set the vendor field to the VendorProfile object belonging to the authenticated user
        try:
            vendor = VendorProfile.objects.get(vendor_id = self.request.user.id)
        except VendorProfile.DoesNotExist as e:
            return Response("Profile not found !!", status=status.HTTP_404_NOT_FOUND)
        serializer.save(vendor=vendor)
    

class OtherServiceGetView(RetrieveDestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = OtherServices.objects.all().order_by('name')
    serializer_class = OtherServiceSerializer
    lookup_field = 'pk'


class VendorServiceListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        try:
            vendor_profile = VendorProfile.objects.get(vendor_id=request.user.id)
            selected_services = vendor_profile.specialised_on.filter(is_active=True)
        except VendorProfile.DoesNotExist:
            selected_services = Service.objects.none()
        
        all_available_services = Service.objects.filter(is_active=True).exclude(id__in=selected_services.values_list('id', flat=True))
        serializer = VendorServiceSerializer({
            'selected_services': selected_services,
            'all_available_services': all_available_services
        })
        return Response(serializer.data)

class VendorServiceRemoveView(UpdateAPIView):
    permission_classes = [IsAuthenticated]
        
    def put(self, request, *args, **kwargs):
        try:
            vendor_profile = VendorProfile.objects.get(vendor_id=request.user.id)
            if request.data.get('action') == 'remove':
                service = Service.objects.get(slug=request.data.get('service_slug'))
                vendor_profile.specialised_on.remove(service)
            elif request.data.get('action') == 'add':
                service_slugs = request.data.get('service_slugs')
                services = Service.objects.filter(slug__in = service_slugs)
                vendor_profile.specialised_on.add(*services)
            selected_services = vendor_profile.specialised_on.filter(is_active = True).order_by('name')
            all_available_services = Service.objects.filter(is_active=True).exclude(id__in=selected_services.values_list('id', flat=True))
            # serializer = ServiceSerializer(services, many=True)
            serializer = VendorServiceSerializer({
                'selected_services': selected_services,
                'all_available_services': all_available_services
            })
            return Response(serializer.data, status=status.HTTP_200_OK)
        except VendorProfile.DoesNotExist:
            return Response("Vendor profile does not exist", status=status.HTTP_404_NOT_FOUND)
        except Service.DoesNotExist:
            return Response("Service does not exist", status=status.HTTP_404_NOT_FOUND)