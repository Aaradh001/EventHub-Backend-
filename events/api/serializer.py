from rest_framework import serializers
from ..models import EventCategory, Event



class EventCategorySerialiser(serializers.ModelSerializer):
    class Meta:
        model = EventCategory
        fields = "__all__"

class EventSerialiser(serializers.Serializer):
    class Meta:
        model = Event
        fields = "__all__"

        extra_kwargs = {
            'event_cat': {'required': True},
            'name': {'required': True},
            'start_date': {'required': True},
            'end_date': {'required': True},
        }