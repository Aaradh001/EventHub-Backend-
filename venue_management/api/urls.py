from django.urls import path
from . import views


urlpatterns = [
    path("venues/", views.VenueListView.as_view(), name="venues"),
    path('venue-detail/<int:pk>/', views.VenueRetrieveAPIView.as_view(), name='venue-detail'),
    path('venue-images/', views.VenueImageListAPIView.as_view(), name='venue-image-list'),
]