 
# Register your models here.
from django.contrib import admin
from django.db.models import Count, F
from .models import *
# from .models import UserTypeMaster, LoginTypeMaster, AccessTypeMaster


@admin.register(UserTypeMaster)
class UserTypeMasterAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'usertype_text',
        'user_type',
        'status',
        'record_status',
        'create_date',
        'update_date'
    )
    list_filter = ('status', 'record_status')
    search_fields = ('usertype_text', 'user_type')
    ordering = ('-create_date',)
    readonly_fields = ('create_date', 'update_date')


@admin.register(LoginTypeMaster)
class LoginTypeMasterAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'remark',
        'record_status',
        'create_date',
        'update_date'
    )
    list_filter = ('record_status',)
    search_fields = ('name',)
    ordering = ('-create_date',)
    readonly_fields = ('create_date', 'update_date')


@admin.register(AccessTypeMaster)
class AccessTypeMasterAdmin(admin.ModelAdmin):
    list_display = (
        'accesstype_id',
        'accesstype_text',
        'access_type',
        'status',
        'record_status',
        'create_date',
        'update_date'
    )
    list_filter = ('status', 'record_status')
    search_fields = ('accesstype_text', 'access_type')
    ordering = ('-create_date',)
    readonly_fields = ('create_date', 'update_date')


@admin.register(Facility)
class FacilityAdmin(admin.ModelAdmin):
    list_display = ('facility_name', 'sr_no', 'remarks')
    search_fields = ('facility_name',)
    ordering = ('sr_no',)


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = (
        'room_id',
        'room_type',
        'ac_non_ac',
        'room_rent',
        'facility',
        'occupied_count',
        'capacity',
        'is_full',
    )
    list_filter = ('room_type', 'ac_non_ac')
    search_fields = ('room_id', 'facility__facility_name')



@admin.register(Tenant)
class TenantAdmin(admin.ModelAdmin):
    list_display = (
        'first_name', 'last_name', 'phone_no',
        'email', 'room', 'pending_rent', 'total_paid'
    )
    list_filter = ('room', 'state', 'city')
    search_fields = ('first_name', 'last_name', 'phone_no', 'email', 'aadhar_no')
    readonly_fields = ('pending_rent', 'total_paid')

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "room":
            available_room_ids = []
            for room in Room.objects.prefetch_related("tenants"):
                if room.occupied_count() < room.capacity():
                    available_room_ids.append(room.id)

            kwargs["queryset"] = Room.objects.filter(id__in=available_room_ids)

        return super().formfield_for_foreignkey(db_field, request, **kwargs)



@admin.register(ElectricityBill)
class ElectricityBillAdmin(admin.ModelAdmin):
    list_display = ('tenant', 'date_month', 'previous_reading', 'current_reading', 'unit_charge',)
    list_filter = ('date_month',)
    search_fields = ('tenant__first_name', 'tenant__phone_no')


@admin.register(Tenant_history)
class TenantHistoryAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'tenant',
        'changed_field',
        'old_value',
        'new_value',
        'changed_at',
    )
    list_filter = ('changed_field', 'changed_at')
    search_fields = ('tenant__first_name', 'tenant__last_name')
    readonly_fields = ('changed_at',)