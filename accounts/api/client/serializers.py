from rest_framework import serializers
from accounts.models import ClientProfile, Account
from django.contrib.auth import get_user_model

User = get_user_model()

class ClientRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientProfile
        fields = ['first_name', 'last_name']
        extra_kwargs = {
            'password':{ 'write_only':True}
        }
        
    
    def create(self, validated_data):

        password = validated_data.pop('password',None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
            instance.save()
            return instance
        else:
            raise serializers.ValidationError({"password": "password is not valid"})
        



class AccountSerializer(serializers.ModelSerializer):

    user_role = serializers.CharField(default='CLIENT')

    class Meta:
        model = Account
        fields = ['username', 'email', 'phone_number', 'user_role']
        extra_kwargs = {
            'username': {'required': True},
            'email': {'required': True},
            'phone_number': {'required': True},
            'user_role': {'read_only': True}
        }

class ClientProfileSerializer(serializers.ModelSerializer):
    account = AccountSerializer()

    class Meta:
        model = ClientProfile
        fields = ['account', 'first_name', 'last_name']

    def create(self, validated_data):
        account_data = validated_data.pop('account')
        print(account_data)
        account_data['user_role'] = 'CLIENT'  # Set user_role to CLIENT
        account = Account.objects.create(**account_data)
        client_profile = ClientProfile.objects.create(client=account, **validated_data)
        return client_profile

    # def update(self, instance, validated_data):
    #     account_data = validated_data.pop('account')
    #     account = instance.client
    #     account.username = account_data.get('username', account.username)
    #     account.email = account_data.get('email', account.email)
    #     account.phone_number = account_data.get('phone_number', account.phone_number)
    #     account.user_role = account_data.get('user_role', account.user_role)
    #     account.save()

    #     instance.first_name = validated_data.get('first_name', instance.first_name)
    #     instance.last_name = validated_data.get('last_name', instance.last_name)
    #     instance.profile_pic = validated_data.get('profile_pic', instance.profile_pic)
    #     instance.area_of_preference = validated_data.get('area_of_preference', instance.area_of_preference)
    #     instance.save()

    #     return instance
