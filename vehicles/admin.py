from django.contrib import admin
from .models import Vehicle, VehicleType, VehicleStatus, OdometerEntry, Service, ServiceFile, ServiceField
# Register your models here.
admin.site.register(Vehicle)
admin.site.register(VehicleType)
admin.site.register(VehicleStatus)
admin.site.register(OdometerEntry)
admin.site.register(Service)
admin.site.register(ServiceFile)
admin.site.register(ServiceField)
