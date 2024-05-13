from django.urls import path
from . import views



urlpatterns = [
    path('event-types/', views.EventCategoryListCreateView.as_view(), name='event_types'),
    path('events/', views.EventListCreateView.as_view(), name='events'),
]