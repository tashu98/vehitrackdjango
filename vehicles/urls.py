from django.urls import path
from .views import DashboardView, VehicleListView, VehicleTypeListView, VehicleStatusListView

urlpatterns = [
    path('dashboard', DashboardView.as_view(), name='dashboard'),
    path('list', VehicleListView.as_view(), name='vehicle_list'),
    path('types', VehicleTypeListView.as_view(), name='vehicle_types_list'),
    path('statuses', VehicleStatusListView.as_view(), name='vehicle_statuses_list'),
]