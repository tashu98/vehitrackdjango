from django.db import models


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


class OdometerEntry(models.Model):
    value = models.IntegerField()
    date = models.DateTimeField()
    is_void = models.BooleanField()
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)


class Service(models.Model):
    service_date = models.DateTimeField()
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)


class ServiceFile(models.Model):
    path = models.CharField(max_length=255)
    hash = models.CharField(max_length=255)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)


class ServiceField(models.Model):
    name = models.CharField(max_length=255)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
