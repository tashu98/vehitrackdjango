from django.contrib import messages
from django.shortcuts import get_object_or_404, render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import *
from .models import Vehicle, VehicleType, VehicleStatus


# Create your views here.
class DashboardView(LoginRequiredMixin, View):
    template_name = 'vehicles/dashboard.html'

    def get(self, request, *args, **kwargs):
        # Retrieve the total number of vehicles
        total_vehicles = Vehicle.objects.count()
        total_users = User.objects.count()
        active_users = User.objects.filter(is_active=True).count()
        active_vehicles = Vehicle.objects.filter(vehicle_status__name='Active').count()

        service_costs_7_days = Vehicle.get_total_service_costs_last_days(7)
        service_costs_30_days = Vehicle.get_total_service_costs_last_days(30)

        mileage_7_days = Vehicle.get_total_km_last_days(7)
        mileage_30_days = Vehicle.get_total_km_last_days(30)



        context = {
            'total_vehicles': total_vehicles,
            'total_users': total_users,
            'service_costs_7_days': service_costs_7_days,
            'service_costs_30_days': service_costs_30_days,
            'mileage_7_days': mileage_7_days,
            'mileage_30_days': mileage_30_days,
            'active_users': active_users,
            'active_vehicles': active_vehicles,
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
            return redirect('vehicle_types_list')

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
        services = Service.objects.all()

        context = {
            'services': services,
        }
        # Retrieve the list of vehicle statuses from the database
        return render(request, self.template_name, context)


class ServiceDetailsView(LoginRequiredMixin, View):
    template_name = 'vehicles/service_details.html'

    def get(self, request, *args, **kwargs):
        service = get_object_or_404(Service, pk=kwargs['id'])
        # Retrieve the list of vehicle statuses from the database
        service_fields = service.get_service_fields()
        context = {
            'service': service,
            'service_fields': service_fields
        }
        return render(request, self.template_name, context)


class VehicleDetailsView(View):
    template_name = 'vehicles/vehicle_details.html'
    odometer_entry_form_class = OdometerEntryForm
    change_status_form_class = ChangeStatusForm

    def get(self, request, *args, **kwargs):
        vehicle = get_object_or_404(Vehicle, pk=kwargs['id'])
        vehicle_statuses = VehicleStatus.objects.all()

        odometer_entry_form = self.odometer_entry_form_class()
        change_status_form = self.change_status_form_class()

        last_odometer_entry = vehicle.get_last_odometer_entry().value
        odometer_from_7_days = vehicle.get_odometer_entry_from_date(
            datetime.date.today() - datetime.timedelta(days=7)).value
        odometer_from_30_days = vehicle.get_odometer_entry_from_date(
            datetime.date.today() - datetime.timedelta(days=30)).value
        km_from_7_days = vehicle.get_km_per_day_from_last_days(7)
        km_from_30_days = vehicle.get_km_per_day_from_last_days(30)
        service_cost_7_days = vehicle.get_service_cost_from_last_days(7)
        service_cost_30_days = vehicle.get_service_cost_from_last_days(30)
        cost_per_km_7_days = vehicle.get_cost_per_km_from_last_days(7)
        cost_per_km_30_days = vehicle.get_cost_per_km_from_last_days(30)

        services = vehicle.get_services()
        odometer_entries = vehicle.get_all_odometer_entries()

        context = {
            'vehicle': vehicle,
            'vehicle_statuses': vehicle_statuses,

            'odometer_entry_form': odometer_entry_form,
            'change_status_form': change_status_form,

            'last_odometer_entry': last_odometer_entry,
            'odometer_from_7_days': odometer_from_7_days,
            'odometer_from_30_days': odometer_from_30_days,
            'km_per_day_7': km_from_7_days,
            'km_per_day_30': km_from_30_days,
            'service_cost_7_days': service_cost_7_days,
            'service_cost_30_days': service_cost_30_days,
            'cost_per_km_7_days': cost_per_km_7_days,
            'cost_per_km_30_days': cost_per_km_30_days,
            'services': services,
            'odometer_entries': odometer_entries,
        }

        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        vehicle = Vehicle.objects.get(id=kwargs['id'])
        vehicle_statuses = VehicleStatus.objects.all()

        odometer_entry_form = self.odometer_entry_form_class(request.POST)
        change_status_form = self.change_status_form_class(request.POST)

        if odometer_entry_form.is_valid():
            value = odometer_entry_form.cleaned_data['value']
            date = odometer_entry_form.cleaned_data['date']

            vehicle.add_odometer_entry(value, date)
            return redirect('vehicle_details', id=kwargs['id'])

        if change_status_form.is_valid():
            new_status = change_status_form.cleaned_data['vehicle_status']
            vehicle.change_status(new_status)

            return redirect('vehicle_details', id=kwargs['id'])

        last_odometer_entry = vehicle.get_last_odometer_entry().value
        odometer_from_7_days = vehicle.get_odometer_entry_from_date(
            datetime.date.today() - datetime.timedelta(days=7)).value
        odometer_from_30_days = vehicle.get_odometer_entry_from_date(
            datetime.date.today() - datetime.timedelta(days=30)).value
        km_from_7_days = vehicle.get_km_per_day_from_last_days(7)
        km_from_30_days = vehicle.get_km_per_day_from_last_days(30)
        service_cost_7_days = vehicle.get_service_cost_from_last_days(7)
        service_cost_30_days = vehicle.get_service_cost_from_last_days(30)
        cost_per_km_7_days = vehicle.get_cost_per_km_from_last_days(7)
        cost_per_km_30_days = vehicle.get_cost_per_km_from_last_days(30)

        services = vehicle.get_services()
        odometer_entries = vehicle.get_all_odometer_entries()

        context = {
            'vehicle': vehicle,
            'vehicle_statuses': vehicle_statuses,

            'odometer_entry_form': odometer_entry_form,
            'change_status_form': change_status_form,

            'last_odometer_entry': last_odometer_entry,
            'odometer_from_7_days': odometer_from_7_days,
            'odometer_from_30_days': odometer_from_30_days,
            'km_per_day_7': km_from_7_days,
            'km_per_day_30': km_from_30_days,
            'service_cost_7_days': service_cost_7_days,
            'service_cost_30_days': service_cost_30_days,
            'cost_per_km_7_days': cost_per_km_7_days,
            'cost_per_km_30_days': cost_per_km_30_days,
            'services': services,
            'odometer_entries': odometer_entries,
        }

        return render(request, self.template_name, context)



class NewServiceView(LoginRequiredMixin, View):
    template_name = 'vehicles/new_service.html'
    service_form_field = NewServiceForm

    def get(self, request, *args, **kwargs):
        vehicle = Vehicle.objects.get(id=kwargs['id'])
        # Retrieve the list of vehicle statuses from the database
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        vehicle = Vehicle.objects.get(id=kwargs['id'])

        service_entry_form = self.service_form_field(request.POST)

        if service_entry_form.is_valid():
            date = service_entry_form.cleaned_data['service_date']

            vehicle.add_service_entry(date)
            return redirect('vehicle_details', id=kwargs['id'])

        return render(request, self.template_name)
