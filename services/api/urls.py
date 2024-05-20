from django.urls import path
from . import views

urlpatterns = [
    path('', views.ServiceList.as_view(), name='services'),
    path('service/<int:pk>/', views.ServiceGetOrUpdate.as_view(), name='services'),
]