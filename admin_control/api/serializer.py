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

class VendorSerializer(serializers.ModelSerializer):
    vendor = AccountSerializer()
    class Meta:
        model = VendorProfile
        fields = "__all__"
        # exclude = ('password', 'user_role')

    def update(self, instance, validated_data):
        instance.vendor.is_active = validated_data['vendor']['is_active']
        instance.vendor.save()
        return instance


class VenueListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Venue
        fields = ['id', 'name', 'full_address', 'city', 'capacity', 'management_company', 'rental_fees', 'reservation_status', 'venue_type', 'is_active']

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

    def update(self, instance, validated_data):
        if self.context['request'].method == 'PATCH':
            if 'is_active' in validated_data:
                instance.is_active = validated_data['is_active']
        elif self.context['request'].method == 'PUT':
            amenities_data = validated_data.pop('amenities', [])
            instance = super().update(instance, validated_data)
            if amenities_data is not None:
                instance.amenities.clear()
                for amenity_data in amenities_data:
                    amenity, created = Amenities.objects.get_or_create(**amenity_data)
                    instance.amenities.add(amenity)
        instance.save()
        return instance

    def create(self, validated_data):
        amenities_data = validated_data.pop('amenities', None)
        venue = Venue.objects.create(**validated_data)

        if amenities_data:
            # Create new amenities if they don't exist in the database
            for amenity_data in amenities_data:
                amenity, created = Amenities.objects.get_or_create(**amenity_data)
                venue.amenities.add(amenity)

        return venue

