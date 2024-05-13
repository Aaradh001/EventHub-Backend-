from django.shortcuts import render
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.views import APIView
from accounts.auth_serializers import MyTokenObtainPairSerializer
from rest_framework.permissions import IsAuthenticated
# from .auth_serializers import UserSerializer
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from django.conf import settings
import jwt
from .models import ClientProfile, VendorProfile
# Create your views here.

User = get_user_model() 

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class CustomTokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_token = serializer.validated_data.get('token')
        # Extract JWT token from the request
        token = request.data.get('refresh')  # Assuming refresh token is passed in the request data

        # Decode the JWT token to extract user information
        decoded_token = jwt.decode(token, verify=False, algorithms=['HS256'], key=settings.JWT_KEY)  # Set verify to False to disable signature verification

        # Retrieve user information from the decoded token
        user_id = decoded_token.get('user_id')  # Adjust based on the actual key used in your JWT token payload
        

        try:
            profile_pic = None
            user = User.objects.get(id=user_id)
            if user.user_role == 'CLIENT':
                profile = ClientProfile.objects.get(client = user)
                profile_pic = profile.profile_pic
            if user.user_role == 'VENDOR':
                profile = VendorProfile.objects.get(vendor = user)
                profile_pic = profile.logo
            # if user.user_role == 'ADMIN':
            #     profile_pic = None
        except Exception as e:
            print(e)

        # Generate a new refresh and access token
        refresh_token = RefreshToken.for_user(user)
        access_token = AccessToken.for_user(user)

        if user.user_role == 'VENDOR':
            refresh_token['isVerified'] = bool(profile.is_verification_completed)


        refresh_token['username'] = user.username
        refresh_token['status'] = user.is_active
        refresh_token['user_role'] = user.user_role
        refresh_token['profile_image'] = profile_pic.url if profile_pic else None
        
        access_token['username'] = user.username
        access_token['status'] = user.is_active
        access_token['user_role'] = user.user_role
        access_token['profile_image'] = profile_pic.url if profile_pic else None

        # Serialize the refresh token and access token
        serialized_refresh_token = str(refresh_token)
        serialized_access_token = str(access_token)

        return Response({'refresh': serialized_refresh_token, 'access': serialized_access_token})



        # # Add additional data to the refresh token payload
        # # Add more additional data as needed

        # # Serialize the refresh token
        # serialized_token = str(refresh_token)

        # return Response({'refresh': serialized_token})