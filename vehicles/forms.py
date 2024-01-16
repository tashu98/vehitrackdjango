# forms.py
from django import forms
from .models import *
from django.contrib.auth.models import User, Permission
from django.contrib.auth.forms import UserCreationForm


class CustomUserCreationForm(UserCreationForm):
    # Add additional fields, e.g., 'is_active' and 'user_permissions'
    is_active = forms.BooleanField(required=False)
    user_permissions = forms.ModelMultipleChoiceField(
        queryset=Permission.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'is_active', 'user_permissions']


class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = ['name', 'vin', 'make', 'model', 'plate', 'vehicle_type', 'vehicle_status']


class VehicleTypeForm(forms.ModelForm):
    class Meta:
        model = VehicleType
        fields = ['name']


class VehicleStatusForm(forms.ModelForm):
    class Meta:
        model = VehicleStatus
        fields = ['name', 'color']


class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['service_date', 'vehicle']


class OdometerEntryForm(forms.ModelForm):
    class Meta:
        model = OdometerEntry
        fields = ['value', 'date']

class NewServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['service_date']


class ChangeStatusForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = ['vehicle_status']
