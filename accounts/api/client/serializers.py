from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from accounts.models import ClientProfile, Account
from django.contrib.auth import get_user_model

User = get_user_model()


class AccountSerializer(serializers.ModelSerializer):

    user_role = serializers.CharField(default='CLIENT')
    class Meta:
        model = Account
        fields = ['username', 'email', 'phone_number', 'password', 'user_role']
        extra_kwargs = {
            'username': {'required': True},
            'email': {'required': True},
            'phone_number': {'required': True},
            'user_role': {'read_only': True},
            'password': {
                'write_only' : True,
                'required' : True
                },
        }

class ClientProfileSerializer(serializers.ModelSerializer):
    client = AccountSerializer()

    class Meta:
        model = ClientProfile
        fields = ['client', 'first_name', 'last_name']

    def create(self, validated_data):
        client_data = validated_data.pop('client')
        client_data['user_role'] = 'CLIENT'  # Set user_role to CLIENT
        account = Account.objects.create(**client_data)
        client_profile = ClientProfile.objects.create(client=account, **validated_data)
        return client_profile

    def update(self, instance, validated_data):
        client_data = validated_data.pop('client')
        account = instance.client
        account.username = client_data.get('username', account.username)
        account.email = client_data.get('email', account.email)
        account.phone_number = client_data.get('phone_number', account.phone_number)
        account.user_role = 'CLIENT'  # Set user_role to CLIENT
        account.save()

        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        # instance.profile_pic = validated_data.get('profile_pic', instance.profile_pic)
        instance.area_of_preference = validated_data.get('area_of_preference', instance.area_of_preference)
        instance.save()

        return instance

class ProfileImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientProfile
        fields = ('profile_pic',)

class AccountDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ('password','user_role', 'is_staff', 'is_superadmin', 'updated_at', 'date_joined')
class ProfileDetailsSerialiser(serializers.ModelSerializer):
    client = AccountDetailsSerializer()
    class Meta:
        model = ClientProfile
        fields = ['client', 'first_name', 'last_name', 'profile_pic', 'area_of_preference']