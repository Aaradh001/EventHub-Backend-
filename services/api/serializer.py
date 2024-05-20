from rest_framework import serializers
from ..models import Service




# class BaseServiceSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = BaseServices
#         fields = "__all__"


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = "__all__"
        read_only_fields = ['slug']