from django.shortcuts import render
from django.contrib.auth import authenticate
from django.http import Http404
from decouple import config
from django.conf import settings
from accounts.models import Account, ClientProfile
from .serializers import ClientProfileSerializer, ProfileDetailsSerialiser, ProfileImageSerializer
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import AuthenticationFailed,ParseError
from rest_framework.views import APIView
from rest_framework.generics import UpdateAPIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from rest_framework import serializers
from django.conf import settings
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.response import Response
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
import requests
import json
# Create your views here.
User = get_user_model()



class GetAccountRoutes(APIView):
    def get(self, request, format = None):
        routes = [
            'api/accounts/login',
            'api/accounts/register',
        ]
        return Response(routes)



class RegisterView(APIView):
    def post(self,request):
        input_data = {}
        for key, value in request.data.items():
            # If the value is a list and has only one element, extract that element
            if isinstance(value, str) and value.startswith('{') and value.endswith('}'):
                input_data[key] = json.loads(value)
            else:
                input_data[key] = value

        serializer = ClientProfileSerializer(data = input_data)

        if serializer.is_valid():
            client = serializer.save()
            area_of_preference = request.POST.get('area_of_preference')
            profile_pic = request.FILES.get('profile_pic')

            if area_of_preference:
                client.area_of_preference = area_of_preference

            if profile_pic:
                client.profile_pic = profile_pic
            client.save()

        else:
            return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)  

        content ={'Message':'User Registered Successfully'}
        return Response(content,status=status.HTTP_201_CREATED)    


class ClientProfileUpdateAPIView(APIView):
    permission_classes = [IsAuthenticated]
    # parser_classes = (MultiPartParser, FormParser)

    def get_object(self, pk):
        try:
            return ClientProfile.objects.get(client__id = pk)
        except ClientProfile.DoesNotExist:
            raise Http404

    def put(self, request, *args, **kwargs):
        client_profile = self.get_object(pk = request.user.id)
        account = client_profile.client
        unique_fields = [field.name for field in account._meta.fields if field.unique and not field.name =='id']
        for field in unique_fields:
            if request.data['client'][field] == getattr(account, field):
                request.data['client'].pop(field)
                
        serializer = ClientProfileSerializer(client_profile, data=request.data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfileImageUpdateView(UpdateAPIView):
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)
    queryset = ClientProfile.objects.all()
    serializer_class = ProfileImageSerializer

    def get_object(self):
        # Get the current user
        try:
            return ClientProfile.objects.get(client__id=self.request.user.id)
        except ClientProfile.DoesNotExist as e:
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
            email = request.data['email']
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
        if user.user_role not in ['CLIENT', 'ADMIN']:
            raise AuthenticationFailed("You don't have permission to enter this page.")

        refresh = RefreshToken.for_user(user)
        refresh["username"] = str(user.username)
        refresh["status"] = bool(user.is_active)
        content = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'isAdmin': user.is_superadmin
            }
        
        return Response(content, status=status.HTTP_200_OK)
    

class AccountDetails(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            user = User.objects.get(id=request.user.id)
            profile = ClientProfile.objects.get(client=user)
            
            data = ProfileDetailsSerialiser(profile).data
            profile_pic = profile.profile_pic
            if profile_pic:
                image_url = request.build_absolute_uri('/')[:-1] + profile_pic.url
                data['profile_pic'] = image_url
            else:
                data['profile_pic'] = ''
            return Response(data)
        except (User.DoesNotExist, ClientProfile.DoesNotExist) as e:
            return Response({"error": "User or profile not found."}, status=404)
        except Exception as e:
            return Response({"error": str(e)}, status=500)

class GoogleAuth(APIView):

    def post(self, request):
        accountExist = True
        try:
            google_request = google_requests.Request()
            id_info = id_token.verify_oauth2_token(
                request.data['credential'], google_request, settings.GOOGLE_OAUTH2_CLIENT_ID, clock_skew_in_seconds=10)
            email = id_info['email']

        except KeyError:
            raise ParseError('Check credential')

        if not Account.objects.filter(email=email).exists():
            accountExist = False
            username = id_info['email'].split('@')[0]
            name = id_info['name']
            user = Account.objects.create(
                email=email, 
                username=username, 
                user_role = 'CLIENT', 
                )
            user.is_active = True
            user.registration_method='GOOGLE'
            user.save()
            
            client_profile = ClientProfile.objects.create(
                client = user, 
                first_name = id_info['given_name'], 
                last_name = id_info['family_name'],
                )
            

        user = Account.objects.get(email=email)
        if not user.is_active:
            return Response({"error": "User is blocked"}, status=status.HTTP_401_UNAUTHORIZED)

        refresh = RefreshToken.for_user(user)
        # refresh["is_vendor"] = False
        # refresh["name"] = str(user.username)
        # refresh["is_admin"] = False
        refresh["username"] = str(user.username)
        refresh["status"] = bool(user.is_active)
        content = {
            'refresh': str(refresh),
            'user_id': user.id,
            'access': str(refresh.access_token),
            'isAdmin': False,
            'accountExist': accountExist,
        }
        return Response(content, status=status.HTTP_200_OK)


