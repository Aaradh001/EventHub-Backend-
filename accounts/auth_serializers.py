from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from django.contrib.auth import get_user_model
from .models import ClientProfile, VendorProfile

User = get_user_model()


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        try:
            profile_pic = None
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

        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username
        token['user_role'] = user.user_role
        token['status'] = user.is_active
        token['profile_image'] = profile_pic.url if profile_pic else None
        # ...

        return token