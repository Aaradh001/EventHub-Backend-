from rest_framework.generics import ListCreateAPIView, ListAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from ..models import EventCategory, Event
from accounts.models import ClientProfile, VendorProfile
from .serializer import EventCategorySerialiser, EventSerialiser
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework import status


class EventCategoryListCreateView(ListCreateAPIView):
    permission_classes = []
    queryset = EventCategory.objects.filter(is_active = True).order_by('created_at')
    serializer_class = EventCategorySerialiser



class EventListCreateView(ListCreateAPIView):
    serializer_class = EventSerialiser
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        try:
            client = ClientProfile.objects.get(client_id = self.request.user.id)
        except ClientProfile.DoesNotExist as e:
            print(e)
            return Response(status=status.HTTP_404_NOT_FOUND)

        queryset = Event.objects.filter(client_id = client.pk).order_by("created_at")
        print(queryset)
        return queryset
    
    def perform_create(self, serializer):
        try:
            client = ClientProfile.objects.get(client_id=self.request.user.id)
        except ClientProfile.DoesNotExist:
            raise NotFound("Client profile not found")

        serializer.save(client=client)


class EventRetrieveUpdateView(RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Event.objects.all().order_by('created_at')
    serializer_class = EventSerialiser
    lookup_field = 'event_id'

    def perform_update(self, serializer):
        try:
            client = ClientProfile.objects.get(client_id=self.request.user.id)
        except ClientProfile.DoesNotExist:
            raise NotFound("Client profile not found")

        serializer.save(client=client)
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)
