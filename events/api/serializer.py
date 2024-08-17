from rest_framework import serializers
from ..models import EventCategory, Event
from accounts.models import ClientProfile, Account, VendorProfile
from services.models import Service
from accounts.api.client.serializers import ClientProfileSerializer
from jsonschema import validate, ValidationError as JSONSchemaValidationError
from rest_framework.exceptions import ValidationError
from ..models import Requirement


class EventCategorySerialiser(serializers.ModelSerializer):
    class Meta:
        model = EventCategory
        fields = "__all__"

class EventSerialiser(serializers.ModelSerializer):
    # client = ClientProfileSerializer()/
    client = serializers.PrimaryKeyRelatedField(read_only=True)
    
    class Meta:
        model = Event
        fields = "__all__"
        read_only_fields = ['client', 'event_id']

        extra_kwargs = {
            # 'event_cat': {'required': True},
            'name': {'required': True},
            'start_date': {'required': True},
            'end_date': {'required': True},
            # 'guest_count':{'required': True}
        }

    # def update(self, instance, validated_data):
    #     # specialised_on_ids = validated_data.pop('specialised_on')
       
    #     instance.event_cat = validated_data.get('event_cat', instance.event_cat)
    #     instance.thumbnail = validated_data.get('thumbnail', instance.thumbnail)
    #     instance.organiser = validated_data.get('organiser', instance.organiser)
    #     instance.name = validated_data.get('name', instance.name)
    #     instance.description = validated_data.get('description', instance.description)
    #     instance.guest_count = validated_data.get('guest_count', instance.guest_count)
    #     instance.start_date = validated_data.get('start_date', instance.start_date)
    #     instance.end_date = validated_data.get('end_date', instance.end_date)
    #     instance.is_advance_paid = validated_data.get('is_advance_paid', instance.is_advance_paid)
    #     instance.is_final_amount_paid = validated_data.get('is_final_amount_paid', instance.is_final_amount_paid)
    #     instance.status = validated_data.get('status', instance.status)
    #     instance.is_completed = validated_data.get('is_completed', instance.is_completed) 

    #     instance.save()



class RequirementSerializer(serializers.ModelSerializer):
    # service_type = serializers.CharField(write_only=True)

    class Meta:
        model = Requirement
        fields = ['service', 'event', 'req_name', 'start_time', 'end_time', 'requirement_details']

    def validate_requirement_details(self, value):
        # Allow requirement_details to be null
        if value is None:
            return value

        service_id = self.initial_data.get('service')
        try:
            service = Service.objects.get(pk = service_id)
        except Service.DoesNotExist as e:
            print(e)

        if service.service_type == 'CATERING':
            schema = Requirement.CATERING_JSON_SCHEMA
        elif service.service_type == 'DECORATION':
            schema = Requirement.DECORATION_JSON_SCHEMA
        else:
            raise ValidationError("Invalid service type.")
        
        try:
            validate(instance=value, schema=schema)
        except Exception as e:
            raise ValidationError(f"Invalid data for requirement details field: {e}")
        
        return value

    def create(self, validated_data):
        service = validated_data.get('service')
        
        if service:
            requirement_details = validated_data.get('requirement_details')
            if requirement_details is not None:
                if service.service_type == 'CATERING':
                    schema = Requirement.CATERING_JSON_SCHEMA
                elif service.service_type == 'DECORATION':
                    schema = Requirement.DECORATION_JSON_SCHEMA
                else:
                    raise ValidationError("Invalid requirement details.")
                
                try:
                    validate(instance=requirement_details, schema=schema)
                except Exception as e:
                    raise ValidationError(f"Invalid data for requirement details: {e}")
                print("--------------------------------")
                print(validated_data)
        
        requirement = Requirement(**validated_data)
        requirement.save()
        return requirement


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        # fields = '__all__'
        exclude = ['is_staff', 'is_superadmin', 'password']


class VendorSerializer(serializers.ModelSerializer):
    vendor = AccountSerializer(read_only=True)
    
    class Meta:
        model = VendorProfile
        fields = "__all__"
        # If you want to exclude any fields, you can use the `exclude` option
        # exclude = ('password', 'user_role')