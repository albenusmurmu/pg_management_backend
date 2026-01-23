from rest_framework import serializers
from .models import Facility, Room, Tenant, ElectricityBill, UserTypeMaster, LoginTypeMaster, AccessTypeMaster, Tenant_history


class FacilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Facility
        fields = '__all__'


class RoomSerializer(serializers.ModelSerializer):
    facility = serializers.SerializerMethodField(read_only=True)
    facility = serializers.PrimaryKeyRelatedField(
        queryset=Facility.objects.all(),
        required=False,
        allow_null=True
    )

    class Meta:
        model = Room
        fields = '__all__'



class TenantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tenant
        fields = '__all__'


class ElectricityBillSerializer(serializers.ModelSerializer):
    total_units = serializers.SerializerMethodField()
    total_amount = serializers.SerializerMethodField()

    class Meta:
        model = ElectricityBill
        fields = '__all__'

    def get_total_units(self, obj):
        return obj.current_reading - obj.previous_reading

    def get_total_amount(self, obj):
        return self.get_total_units(obj) * obj.unit_charge



class UserTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserTypeMaster
        fields = '__all__'
  


class LoginTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoginTypeMaster
        fields = '__all__'


class AccessTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccessTypeMaster
        fields = '__all__'



class TenantHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Tenant_history
        fields = '__all__'
