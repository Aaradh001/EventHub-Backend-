from rest_framework import serializers
from ..models import EventCategory, Event



class EventCategorySerialiser(serializers.ModelSerializer):
    class Meta:
        model = EventCategory
        fields = "__all__"

class EventSerialiser(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = "__all__"
        read_only_fields = ['client']

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