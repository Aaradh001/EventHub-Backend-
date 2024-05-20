from django.urls import path
from . import views




urlpatterns = [
    path("login/", views.LoginView.as_view(), name="vendor_login"),
    path("details/", views.VendorDetails.as_view(), name="vendor_datails"),

    path("register/", views.RegisterView.as_view(), name="vendor_register"),
    path("profile/updateLogo/", views.ProfileImageUpdateView.as_view(), name="logo_update"),
    path("profile/update/", views.VendorProfileUpdateAPIView.as_view(), name="vendor_update"),
    path("my-services/", views.VendorServiceListView.as_view(), name="my_services"),
    # path("profile/my-services/addService/", views.VendorServiceAddView.as_view(), name="my_services"),
    path('my-services/add-or-remove-service/', views.VendorServiceRemoveView.as_view(), name='remove_vendor_service'),
    path("my-services/other-services/", views.OtherServicesListView.as_view(), name="other_sevices_list"),
    path("my-services/other-service/<int:pk>/", views.OtherServiceGetView.as_view(), name="other_service"),

    path("all-vendors/", views.ProfileImageUpdateView.as_view(), name="logo_update"),

]