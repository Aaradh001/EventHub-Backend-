from django.urls import path
from . import views


urlpatterns = [
    # path('', views.GetAccountRoutes.as_view(), name='account_routes'),
    path("login/", views.LoginView.as_view(), name="admin_login"),
    path("client-management/clients/", views.AdminClientUserListCreateView.as_view(), name="all_clients"),
    path("client-management/client/<int:pk>/", views.ClientRetrieveUpdateAPIView.as_view(), name="client-control"),
    # path("register/", views.RegisterView.as_view(), name="client_register"),
    # path("my-account/update/", views.ClientProfileUpdateAPIView.as_view(), name="client_update"),
    path('venue-management/all-venues/', views.AdminVenueListCreateView.as_view(), name='all_venues'),
    path('venue-management/venue/<int:pk>/', views.VenueRetrieveUpdateAPIView.as_view(), name='venue'),

]