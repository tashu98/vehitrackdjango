from django.urls import path
from .views import *

urlpatterns = [
    path('dashboard', DashboardView.as_view(), name='dashboard'),
    path('list', VehicleListView.as_view(), name='vehicle_list'),
    path('vehicle', VehicleDetailsView.as_view(), name='vehicle_details'),
    path('types', VehicleTypeListView.as_view(), name='vehicle_types_list'),
    path('statuses', VehicleStatusListView.as_view(), name='vehicle_statuses_list'),
    path('services', ServicesListView.as_view(), name='services_list'),
    path('new-service', NewServiceView.as_view(), name='new_service'),
    path('service', ServiceDetailsView.as_view(), name='service_details'),
]