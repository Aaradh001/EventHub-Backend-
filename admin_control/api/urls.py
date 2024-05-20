from django.urls import path
from . import views


urlpatterns = [
    # path('', views.GetAccountRoutes.as_view(), name='account_routes'),
    path("login/", views.LoginView.as_view(), name="admin_login"),
    path("client-management/clients/", views.AdminClientUserListCreateView.as_view(), name="all_clients"),
    path("client-management/client/<int:pk>/", views.ClientRetrieveUpdateAPIView.as_view(), name="client-control"),
    path("vendor-management/vendors/", views.AdminVendorUserListCreateView.as_view(), name="all_vendors"),
    path("vendor-management/vendor/<int:pk>/", views.VendorRetrieveUpdateAPIView.as_view(), name="vendor-control"),
    # path("register/", views.RegisterView.as_view(), name="client_register"),
    # path("my-account/update/", views.ClientProfileUpdateAPIView.as_view(), name="client_update"),
    path('venue-management/all-venues/', views.AdminVenueListCreateView.as_view(), name='all_venues'),
    path('venue-management/venue/<int:pk>/', views.VenueRetrieveUpdateAPIView.as_view(), name='venue'),
    path('venue-management/venue-images/', views.VenueImageListCreateAPIView.as_view(), name='venue_image_create_list'),
    path('venue-management/venue-image/<int:pk>/', views.VenueImageRetrieveUpdateAPIView.as_view(), name='venue_image_update'),
    path('venue-management/all-amenities/', views.AdminAmenityListCreateView.as_view(), name='all_amenities'),
    # path('venue-management/venue/<int:pk>/', views.VenueRetrieveUpdateAPIView.as_view(), name='venue'),

]