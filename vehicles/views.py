from django.shortcuts import render
from django.views import View
from .models import Vehicle


# Create your views here.
class VehicleListView(View):
    template_name = 'vehicles/vehicle_list.html'

    def get(self, request, *args, **kwargs):
        # Retrieve the list of vehicles from the database
        vehicles = Vehicle.objects.all()

        # Pass the list of vehicles to the template
        context = {'vehicles': vehicles}
        return render(request, self.template_name, context)
