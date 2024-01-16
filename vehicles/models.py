from django.db import models
import datetime
from decimal import Decimal


# Create your models here.
class VehicleType(models.Model):
    name = models.CharField(max_length=255)


class VehicleStatus(models.Model):
    name = models.CharField(max_length=255)
    color = models.CharField(max_length=255)


class Vehicle(models.Model):
    name = models.CharField(max_length=255)
    vin = models.CharField(max_length=17, unique=True)
    make = models.CharField(max_length=255)
    model = models.CharField(max_length=255)
    plate = models.CharField(max_length=10, unique=True)
    vehicle_type = models.ForeignKey(VehicleType, on_delete=models.CASCADE)
    vehicle_status = models.ForeignKey(VehicleStatus, on_delete=models.CASCADE)

    @classmethod
    def get_total_service_costs_last_days(cls, days):
        vehicles = cls.objects.all()
        total_cost = 0
        for vehicle in vehicles:
            total_cost += vehicle.get_service_cost_from_last_days(days)
        return total_cost

    @classmethod
    def get_total_km_last_days(cls, days):
        vehicles = cls.objects.all()
        total_km = 0
        for vehicle in vehicles:
            total_km += vehicle.get_km_per_day_from_last_days(days)
        return total_km

    def add_odometer_entry(self, value, date, is_void=False):
        last_odometer_entry = self.get_last_odometer_entry()
        if last_odometer_entry is not None:
            if value < last_odometer_entry.value:
                raise ValueError("Odometer value cannot be less than last odometer entry")
        odometer_entry = OdometerEntry(value=value, date=date, is_void=is_void, vehicle=self)
        odometer_entry.save()

    def add_service_entry(self, date):
        service = Service(service_date=date, vehicle=self)
        service.save()

    def change_status(self, vehicle_status):
        self.vehicle_status = vehicle_status
        self.save()

    def get_last_odometer_entry(self):
        if self.odometerentry_set.count() == 0:
            return None
        return self.odometerentry_set.order_by('-date').first()

    def get_odometer_entry_from_date(self, date):
        if self.odometerentry_set.count() == 0:
            return None
        return self.odometerentry_set.filter(date__lte=date).order_by('-date').first()

    def get_all_odometer_entries(self):
        return self.odometerentry_set.order_by('date')

    def get_km_per_day_from_last_days(self, days):
        odometer_entries = self.get_all_odometer_entries()
        last_odometer_entry = self.get_last_odometer_entry()
        if last_odometer_entry is None:
            return 0
        last_odometer_entry_date = last_odometer_entry.date
        km_per_day = 0
        for odometer_entry in odometer_entries:
            if odometer_entry.date > last_odometer_entry_date - datetime.timedelta(days=days):
                km_per_day += odometer_entry.value
        return km_per_day / days

    def get_services(self):
        return self.service_set.order_by('-service_date')

    def get_service_cost_from_last_days(self, days):
        services = self.get_services()
        last_service = services.first()
        if last_service is None:
            return 0
        last_service_date = last_service.service_date
        cost = 0
        for service in services:
            if service.service_date > last_service_date - datetime.timedelta(days=days):
                cost += service.get_service_cost()
        return cost

    def get_cost_per_km_from_last_days(self, days):
        km_per_day = self.get_km_per_day_from_last_days(days)
        if km_per_day == 0:
            return Decimal(0)
        return self.get_service_cost_from_last_days(days) / Decimal(km_per_day)


class OdometerEntry(models.Model):
    value = models.IntegerField()
    date = models.DateTimeField()
    is_void = models.BooleanField()
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)


class Service(models.Model):
    service_date = models.DateTimeField()
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)

    def get_service_fields(self):
        return self.servicefield_set.all()

    def get_service_fields_names_string(self):
        service_fields = self.get_service_fields()
        service_fields_names = []
        for service_field in service_fields:
            service_fields_names.append(service_field.name)
        return ', '.join(service_fields_names)

    def get_service_cost(self):
        cost = 0
        for service_field in self.get_service_fields():
            cost += service_field.cost
        return cost


class ServiceFile(models.Model):
    service = models.ForeignKey('Service', on_delete=models.CASCADE)
    file = models.FileField(upload_to='service_files/')

    def __str__(self):
        return self.file.name


class ServiceField(models.Model):
    name = models.CharField(max_length=255)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
