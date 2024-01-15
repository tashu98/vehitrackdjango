from django.contrib import messages
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import *
from .models import Vehicle, VehicleType, VehicleStatus


# Create your views here.
class DashboardView(LoginRequiredMixin, View):
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


class VehicleListView(LoginRequiredMixin, View):
    template_name = 'vehicles/vehicle_list.html'
    form_class = VehicleForm

    def get(self, request, *args, **kwargs):
        vehicles = Vehicle.objects.all()  # Replace with your actual queryset
        form = self.form_class()

        vehicle_types = VehicleType.objects.all()
        vehicle_statuses = VehicleStatus.objects.all()

        context = {
            'vehicles': vehicles,
            'form': form,
            'vehicle_types': vehicle_types,
            'vehicle_statuses': vehicle_statuses,
        }

        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Vehicle added successfully.")
            return redirect('vehicle_list')

        # If form is not valid, render the same page with the error messages
        messages.error(request, "There were errors in the form. Please correct them.")
        vehicles = Vehicle.objects.all()
        vehicle_types = VehicleType.objects.all()
        vehicle_statuses = VehicleStatus.objects.all()

        context = {
            "vehicles": vehicles,
            "form": form,
            "vehicle_types": vehicle_types,
            "vehicle_statuses": vehicle_statuses
        }

        return render(request, self.template_name, context)


class VehicleTypeListView(LoginRequiredMixin, View):
    template_name = 'vehicles/vehicle_type_list.html'
    form_class = VehicleTypeForm

    def get(self, request, *args, **kwargs):
        # Retrieve the list of vehicle types from the database
        vehicle_types = VehicleType.objects.all()

        # Create an instance of the form
        form = self.form_class()

        # Create a dictionary to store the count of vehicles for each vehicle type
        vehicle_type_count = {}

        # Populate the dictionary with counts
        for vehicle_type in vehicle_types:
            vehicle_type_count[vehicle_type] = Vehicle.objects.filter(vehicle_type=vehicle_type).count()

        # Pass the list of vehicle types, the form, and the counts to the template
        context = {'vehicle_types': vehicle_types, 'form': form, 'vehicle_type_count': vehicle_type_count}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        # Create an instance of the form with the submitted data
        form = self.form_class(request.POST)

        # Check if the form is valid
        if form.is_valid():
            # Save the new vehicle type
            form.save()
            # Redirect to the same page (GET) after successful form submission
            return redirect('your_vehicle_type_list_url_name')

        # If form is not valid, render the same page with the error messages
        vehicle_types = VehicleType.objects.all()

        # Replicate the logic to count vehicles
        vehicle_type_count = {}
        for vehicle_type in vehicle_types:
            vehicle_type_count[vehicle_type] = Vehicle.objects.filter(vehicle_type=vehicle_type).count()

        context = {'vehicle_types': vehicle_types, 'form': form, 'vehicle_type_count': vehicle_type_count}
        return render(request, self.template_name, context)


class VehicleStatusListView(LoginRequiredMixin, View):
    template_name = 'vehicles/vehicle_status_list.html'

    def get(self, request, *args, **kwargs):
        # Retrieve the list of vehicle statuses from the database
        vehicle_statuses = VehicleStatus.objects.all()

        # Create an instance of the form
        form = VehicleStatusForm()

        # Pass the list of vehicle statuses and the form to the template
        context = {'vehicle_statuses': vehicle_statuses, 'form': form}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        # Create an instance of the form with the submitted data
        form = VehicleStatusForm(request.POST)

        # Check if the form is valid
        if form.is_valid():
            # Save the new vehicle status
            form.save()
            # Redirect to the same page (GET) after successful form submission
            return redirect('vehicle_statuses_list')

        # If form is not valid, render the same page with the error messages
        vehicle_statuses = VehicleStatus.objects.all()

        context = {'vehicle_statuses': vehicle_statuses, 'form': form}
        return render(request, self.template_name, context)


class ServicesListView(LoginRequiredMixin, View):
    template_name = 'vehicles/services_list.html'

    def get(self, request, *args, **kwargs):
        # Retrieve the list of vehicle statuses from the database
        return render(request, self.template_name)


class ServiceDetailsView(LoginRequiredMixin, View):
    template_name = 'vehicles/service_details.html'

    def get(self, request, *args, **kwargs):
        # Retrieve the list of vehicle statuses from the database
        return render(request, self.template_name)


class VehicleDetailsView(LoginRequiredMixin, View):
    template_name = 'vehicles/vehicle_details.html'

    def get(self, request, *args, **kwargs):
        # Retrieve the list of vehicle statuses from the database
        return render(request, self.template_name)


class NewServiceView(LoginRequiredMixin, View):
    template_name = 'vehicles/new_service.html'

    def get(self, request, *args, **kwargs):
        # Retrieve the list of vehicle statuses from the database
        return render(request, self.template_name)
