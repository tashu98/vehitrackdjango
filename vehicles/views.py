from django.shortcuts import render
from django.views import View
from .models import Vehicle, VehicleType, VehicleStatus


# Create your views here.
class DashboardView(View):
    template_name = 'vehicles/dashboard.html'

    def get(self, request, *args, **kwargs):
        # Example data for the dashboard
        total_vehicles = Vehicle.objects.count()
        vehicle_types = VehicleType.objects.all()
        vehicle_statuses = VehicleStatus.objects.all()

        # Pass the data to the template
        context = {
            'total_vehicles': total_vehicles,
            'vehicle_types': vehicle_types,
            'vehicle_statuses': vehicle_statuses,
        }
        return render(request, self.template_name, context)
class VehicleListView(View):
    template_name = 'vehicles/vehicle_list.html'

    def get(self, request, *args, **kwargs):
        # Retrieve the list of vehicles from the database
        vehicles = Vehicle.objects.all()

        # Pass the list of vehicles to the template
        context = {'vehicles': vehicles}
        return render(request, self.template_name, context)


class VehicleTypeListView(View):
    template_name = 'vehicles/vehicle_type_list.html'

    def get(self, request, *args, **kwargs):
        # Retrieve the list of vehicle types from the database
        vehicle_types = VehicleType.objects.all()

        # Pass the list of vehicle types to the template
        context = {'vehicle_types': vehicle_types}
        return render(request, self.template_name, context)


class VehicleStatusListView(View):
    template_name = 'vehicles/vehicle_status_list.html'

    def get(self, request, *args, **kwargs):
        # Retrieve the list of vehicle statuses from the database
        vehicle_statuses = VehicleStatus.objects.all()

        # Pass the list of vehicle statuses to the template
        context = {'vehicle_statuses': vehicle_statuses}
        return render(request, self.template_name, context)

class ServicesListView(View):
    template_name = 'vehicles/services_list.html'

    def get(self, request, *args, **kwargs):
        # Retrieve the list of vehicle statuses from the database
        return render(request, self.template_name)

class UsersListView(View):
    template_name = 'vehicles/users_list.html'

    def get(self, request, *args, **kwargs):
        # Retrieve the list of vehicle statuses from the database
        return render(request, self.template_name)

class ServiceDetailsView(View):
    template_name = 'vehicles/service_details.html'

    def get(self, request, *args, **kwargs):
        # Retrieve the list of vehicle statuses from the database
        return render(request, self.template_name)

class UserDetailsView(View):
    template_name = 'vehicles/user_details.html'

    def get(self, request, *args, **kwargs):
        # Retrieve the list of vehicle statuses from the database
        return render(request, self.template_name)

class VehicleDetailsView(View):
    template_name = 'vehicles/vehicle_details.html'

    def get(self, request, *args, **kwargs):
        # Retrieve the list of vehicle statuses from the database
        return render(request, self.template_name)

class NewServiceView(View):
    template_name = 'vehicles/new_service.html'

    def get(self, request, *args, **kwargs):
        # Retrieve the list of vehicle statuses from the database
        return render(request, self.template_name)