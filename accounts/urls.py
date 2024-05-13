from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from . import views



urlpatterns = [
    path('access-token/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh-token/', views.CustomTokenRefreshView.as_view(), name='token_refresh'),
]