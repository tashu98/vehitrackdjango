from django.urls import path
from .views import DashboardView, VehicleListView, VehicleTypeListView, VehicleStatusListView,UsersListView,ServicesListView

urlpatterns = [
    path('dashboard', DashboardView.as_view(), name='dashboard'),
    path('list', VehicleListView.as_view(), name='vehicle_list'),
    path('vehicle', VehicleListView.as_view(), name='vehicle_details'),
    path('types', VehicleTypeListView.as_view(), name='vehicle_types_list'),
    path('statuses', VehicleStatusListView.as_view(), name='vehicle_statuses_list'),
    path('services', ServicesListView.as_view(), name='services_list'),
    path('service', ServicesListView.as_view(), name='service_details'),
    path('users', UsersListView.as_view(), name='users_list'),
    path('user', UsersListView.as_view(), name='users_details'),
]