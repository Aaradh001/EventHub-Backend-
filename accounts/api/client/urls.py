from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from . import views
# from accounts import views as main_views


urlpatterns = [
    path('', views.GetAccountRoutes.as_view(), name='account_routes'),
    path('account-routes/', views.GetAccountRoutes.as_view(), name='account_routes'),
    path('my-account/', views.AccountDetails.as_view(), name='account_details'),
    path("my-account/update/", views.ClientProfileUpdateAPIView.as_view(), name="client_update"),
    path("my-account/update-profile-image/", views.ProfileImageUpdateView.as_view(), name="profile_image_update"),

    path("client-login/", views.LoginView.as_view(), name="user-login"),
    path("google-login/", views.GoogleAuth.as_view(), name="google_auth"),
    path("register/", views.RegisterView.as_view(), name="client_register"),
]