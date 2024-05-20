from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView
from ..models import Service
from .serializer import ServiceSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser

# from .serializer import EventCategorySerialiser


# class EventCategoryList(ListAPIView):
#     permission_classes = []
#     queryset = EventCategory.objects.filter(is_active = True).order_by('created_at')
#     serializer_class = EventCategorySerialiser


# class BaseServiceList(ListCreateAPIView):
#     permission_classes = []
#     queryset = BaseServices.objects.filter(is_active = True).order_by('name')
#     serializer_class = BaseServiceSerializer

# class BaseServiceGetOrUpdate(RetrieveUpdateAPIView):
#     # permission_classes = [IsAuthenticated]
#     queryset = BaseServices.objects.filter(is_active = True).order_by('name')
#     serializer_class = BaseServiceSerializer
#     lookup_field = 'pk'


class ServiceList(ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Service.objects.filter(is_active = True).order_by('name')
    serializer_class = ServiceSerializer

class ServiceGetOrUpdate(RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Service.objects.filter(is_active = True).order_by('name')
    serializer_class = ServiceSerializer
    lookup_field = 'pk'