from rest_framework import serializers
from django.contrib.auth import get_user_model
from accounts.models import ClientProfile, VendorProfile
from venue_management.models import Venue, Amenities, VenueImage


User = get_user_model()


class CustomDateTimeField(serializers.DateTimeField):
    def to_representation(self, value):
        # Format the datetime value as required (DD-month-YYYY)
        return value.strftime('%d-%B-%Y')


# User Serializer
class AccountSerializer(serializers.ModelSerializer):
    date_joined = CustomDateTimeField('date_joined')  # Use CustomDateTimeField for date_joined
    class Meta:
        model = User
        # fields = '__all__'
        exclude = ['is_staff', 'is_superadmin', 'password']


class ClientSerializer(serializers.ModelSerializer):
    client = AccountSerializer()
    class Meta:
        model = ClientProfile
        fields = "__all__"
        # exclude = ('password', 'user_role')

    def update(self, instance, validated_data):
        instance.client.is_active = validated_data['client']['is_active']
        instance.client.save()
        return instance


class VenueListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Venue
        fields = ['id', 'name', 'city', 'state', 'thumbnail', 'reservation_status', 'venue_type']

    # def update(self, instance, validated_data):
    #     print(instance)
    #     instance.client.is_active = validated_data['client']['is_active']
    #     instance.client.save()
    #     return instance


# class VenueSerializer(serializers.ModelSerializer):
#     amenities = serializers.PrimaryKeyRelatedField(many=True, queryset=Amenities.objects.all(), required=False)
#     description = serializers.CharField(required=False)
#     class Meta:
#         model = Venue
#         fields = "__all__"


class AmenitiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Amenities
        fields = '__all__'

class VenueImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = VenueImage
        fields = '__all__'
   

class VenueSerializer(serializers.ModelSerializer):
    amenities = AmenitiesSerializer(many=True, required = False)
    description = serializers.CharField(required=False)
    images = VenueImageSerializer(many=True, read_only=True)

    class Meta:
        model = Venue
        fields = '__all__'
