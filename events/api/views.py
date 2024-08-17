from rest_framework.generics import ListCreateAPIView, ListAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError
from ..models import EventCategory, Event, Requirement
from accounts.models import ClientProfile, VendorProfile
from .serializer import EventCategorySerialiser, EventSerialiser, RequirementSerializer, VendorSerializer
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import SearchFilter
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework import status
import datetime

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
    

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        
        try:
            client = ClientProfile.objects.get(client_id=self.request.user.id)
        except ClientProfile.DoesNotExist as e:
            print(e)
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        launched_event = Event.objects.filter(client_id=client.pk, event_stage="LAUNCHED").first()
        all_events_serializer = self.get_serializer(queryset, many=True)
        if launched_event:
            launched_event_serializer = self.get_serializer(launched_event)
            launched_event_data = launched_event_serializer.data
        else:
            launched_event_data = None
        return Response({
            'all_events': all_events_serializer.data,
            'current_event': launched_event_data
        })

    def perform_create(self, serializer):
        try:
            client = ClientProfile.objects.get(client_id=self.request.user.id)
        except ClientProfile.DoesNotExist:
            raise NotFound("Client profile not found")
        
        if Event.objects.filter(client_id=client.pk, event_stage="launched").exists():
            raise ValidationError("There is already an event launched for this client.")
        
        counter = Event.objects.all().count()+1
        event_id = 'EH'+str(round(datetime.datetime.now().timestamp()))+str(counter)

        try:
            serializer.save(client=client, event_id=event_id)
        except ValidationError as e:
            print("Validation error: ", e)
            raise e


class EventRetrieveUpdateView(RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Event.objects.all().order_by('created_at')
    serializer_class = EventSerialiser
    lookup_field = 'pk'

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




class RequirementBulkCreateListView(APIView):

    def get(self, request, *args, **kwargs):
        event_id = request.data.get('event_id')
        requirements = Requirement.objects.filter(event__event_id=event_id)
        serializer = RequirementSerializer(requirements, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        print("fromn frontend   :",request.data)
        created_objects = []
        errors = []

        for item in request.data:
            item_serializer = RequirementSerializer(data=item)
            if item_serializer.is_valid():
                item_serializer.save()
                created_objects.append(item_serializer.data)
            else:
                errors.append({'detail': item_serializer.errors, 'data': item})

        return Response({'created': created_objects, 'errors': errors}, status=status.HTTP_207_MULTI_STATUS)
    



class VendorList(ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = VendorProfile.objects.filter(vendor__user_role='VENDOR').order_by('vendor__date_joined')
    serializer_class = VendorSerializer
    pagination_class = PageNumberPagination
    filter_backends = [SearchFilter]
    search_fields = ['company_name', 'website']

    def list(self, request, *args, **kwargs):
        self.pagination_class.page_size = 2
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            total_pages = self.paginator.page.paginator.num_pages if self.paginator else 1
            current_page = self.paginator.page.number if self.paginator else 1
            data = {
                'total_pages': total_pages,
                'current_page': current_page,
                'results': serializer.data
            }
            return self.get_paginated_response(data)
        else:
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)

class vendorRetrieveView(RetrieveAPIView):
    queryset = VendorProfile.objects.all()
    serializer_class = VendorSerializer
    permission_classes = [IsAuthenticated]


