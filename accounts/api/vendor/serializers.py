from rest_framework import serializers
from accounts.models import VendorProfile, Account, OtherServices
from django.contrib.auth import get_user_model

User = get_user_model()





class AccountSerializer(serializers.ModelSerializer):

    user_role = serializers.CharField(default='VENDOR')
    class Meta:
        model = Account
        fields = ['username', 'email', 'phone_number', 'password', 'user_role']
        extra_kwargs = {
            'username': {'required': True},
            'email': {'required': True},
            'phone_number': {'required': True},
            'password': {
                'write_only' : True,
                'required' : True
                },
            'user_role': {'read_only': True}
        }

class VendorProfileSerializer(serializers.ModelSerializer):
    vendor = AccountSerializer()
    class Meta:
        model = VendorProfile
        fields = ['vendor', 'company_name', 'website', 'service_capacity']   

    def create(self, validated_data):
        vendor_data = validated_data.pop('vendor')

        # specialised_on_ids = validated_data.pop('specialised_on')
        vendor_data['user_role'] = 'VENDOR'  # Set user_role to VENDOR
        account = Account.objects.create(**vendor_data)
        vendor_profile = VendorProfile.objects.create(vendor = account, **validated_data)
        vendor_profile.save()
        # vendor_profile.specialised_on.set(specialised_on_ids)
        return vendor_profile

    def update(self, instance, validated_data):
        vendor_data = validated_data.pop('vendor')
        # specialised_on_ids = validated_data.pop('specialised_on')
        account = instance.vendor
        account.username = vendor_data.get('username', account.username)
        account.email = vendor_data.get('email', account.email)
        account.phone_number = vendor_data.get('phone_number', account.phone_number)
        account.user_role = 'VENDOR'  # Set user_role to VENDOR
        account.save()

        instance.company_name = validated_data.get('company_name', instance.company_name)
        instance.website = validated_data.get('website', instance.website)
        instance.service_capacity = validated_data.get('service_capacity', instance.service_capacity)
         
        # specialised_on_ids = validated_data.get('specialised_on')
        # instance.specialised_on.set(specialised_on_ids)

        instance.save()

        return instance
    

class AccountDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ('password','user_role', 'is_staff', 'is_superadmin', 'updated_at', 'date_joined')


class ProfileDetailsSerialiser(serializers.ModelSerializer):
    vendor = AccountDetailsSerializer()
    class Meta:
        model = VendorProfile
        fields = '__all__'

class ProfileImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = VendorProfile
        fields = ('logo',)

class OtherServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = OtherServices

        # fields = '__all__'
        fields = ['id', 'name', 'thumbnail', 'is_active', 'cost_per_unit', 'unit_of_measurement', 'other_unit_of_measurement']
        # Set all fields as optional except for 'name' and 'unit_of_measurement'
        extra_kwargs = {
            'thumbnail': {'required': False},
            'is_active': {'required': False},
            'cost_per_unit': {'required': False},
            'other_unit_of_measurement': {'required': False},
        }


from services.models import Service
class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ['name', 'thumbnail', 'unit_of_measurement', 'is_active', 'slug']


class VendorServiceSerializer(serializers.Serializer):
    selected_services = ServiceSerializer(many=True)
    all_available_services = ServiceSerializer(many=True)