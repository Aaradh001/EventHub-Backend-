from rest_framework.generics import ListCreateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from ..models import EventCategory, Event
from .serializer import EventCategorySerialiser, EventSerialiser


class EventCategoryListCreateView(ListCreateAPIView):
    permission_classes = []
    queryset = EventCategory.objects.filter(is_active = True).order_by('created_at')
    serializer_class = EventCategorySerialiser



class EventListCreateView(ListCreateAPIView):
    permission_classes = []
    queryset = Event.objects.filter(status = 'LAUNCHED').order_by('created_at')
    serializer_class = EventSerialiser
    