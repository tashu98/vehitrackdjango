import os
import random
import django
from datetime import datetime, timedelta
from vehicles.models import VehicleType, VehicleStatus, Vehicle, OdometerEntry, Service, ServiceFile, ServiceField

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "VehiTrackDjango.settings")


django.setup()


# Seed data for VehicleType
vehicle_types = ["Sedan", "SUV", "Truck", "Motorcycle", "Van"]
for name in vehicle_types:
    VehicleType.objects.create(name=name)

# Seed data for VehicleStatus
vehicle_statuses = [
    {"name": "Active", "color": "Green"},
    {"name": "Inactive", "color": "Red"},
    {"name": "Under Maintenance", "color": "Yellow"},
    {"name": "Out of Service", "color": "Black"},
    {"name": "Reserved", "color": "Blue"},
]
for status in vehicle_statuses:
    VehicleStatus.objects.create(**status)

# Seed data for Vehicle
for _ in range(10):
    Vehicle.objects.create(
        name=f"Vehicle-{_ + 1}",
        vin=str(random.randint(10000000000000000, 99999999999999999)),
        make=f"Make-{_ + 1}",
        model=f"Model-{_ + 1}",
        plate=f"Plate-{_ + 1}",
        vehicle_type=random.choice(VehicleType.objects.all()),
        vehicle_status=random.choice(VehicleStatus.objects.all()),
    )

# Seed data for OdometerEntry
for _ in range(20):
    OdometerEntry.objects.create(
        value=random.randint(1000, 100000),
        date=datetime.now() - timedelta(days=random.randint(1, 365)),
        is_void=random.choice([True, False]),
        vehicle=random.choice(Vehicle.objects.all()),
    )

# Seed data for Service
for _ in range(15):
    Service.objects.create(
        service_date=datetime.now() - timedelta(days=random.randint(1, 365)),
        vehicle=random.choice(Vehicle.objects.all()),
    )

# Seed data for ServiceFile
for _ in range(30):
    ServiceFile.objects.create(
        service=random.choice(Service.objects.all()),
        file=f"path/to/file{_ + 1}.txt"
    )

# Seed data for ServiceField
for _ in range(25):
    ServiceField.objects.create(
        name=f"ServiceField-{_ + 1}",
        cost=random.uniform(10.0, 500.0),
        service=random.choice(Service.objects.all()),
    )
