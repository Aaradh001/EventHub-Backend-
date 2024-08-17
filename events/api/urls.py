from django.urls import path
from . import views



urlpatterns = [
    path('event-types/', views.EventCategoryListCreateView.as_view(), name='event_types'),
    path('events/', views.EventListCreateView.as_view(), name='events'),
    path('event-detail/<int:pk>/', views.EventRetrieveUpdateView.as_view(), name='retrieve_or_update_event'),
    path('vendors/', views.VendorList.as_view(), name='vendors'),
    path('vendor-detail/<int:pk>/', views.vendorRetrieveView.as_view(), name='retrieve_or_vendor'),
    path('requirements_list_create/', views.RequirementBulkCreateListView.as_view(), name='requirement-bulk-create'),
]