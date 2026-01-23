from django.db import models

from datetime import datetime
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.backends import django
from django.utils.text import slugify
import string
import random
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
# Create your models here.

class BaseModel(models.Model):
    RECORD_STATUS_CHOICES = [
        ('Active', 'Active'),
        ('Deleted', 'Deleted'),
    ]
    created_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True, related_name='%(class)s_created')
    updated_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True, related_name='%(class)s_updated')
    create_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    update_date = models.DateTimeField(auto_now=True, blank=True, null=True)
    record_status = models.CharField(max_length=20, choices=RECORD_STATUS_CHOICES, default='Active')

    class Meta:
        abstract = True
 



class UserTypeMaster(BaseModel):
    
    usertype_text = models.CharField(max_length=100, blank=False, null=False)
    user_type = models.CharField(max_length=20, blank=False, null=False, unique=True)
    status = models.PositiveSmallIntegerField(default=1, blank=True, null=True)
    
    def __str__(self):
        return self.usertype_text


    # def userlist(self):
    #     return UserMaster.objects.filter(user_type=self.user_type, status='1')

    class Meta:
        db_table = "UserTypeMaster"



class LoginTypeMaster(BaseModel):
    name = models.CharField(max_length=100,unique=True)
    remark = models.CharField(max_length=200,blank=True, null=True)

    class Meta:
        db_table = 'LoginTypeMaster'
    def __str__(self):
        return self.name


class AccessTypeMaster(BaseModel):
    accesstype_id = models.AutoField(primary_key=True)
    accesstype_text = models.CharField(max_length=100, blank=False, null=False)
    access_type = models.CharField(max_length=20, blank=False, null=False, unique=True)
    status = models.PositiveSmallIntegerField(default=1, blank=True, null=True)
   

    def __str__(self):
        return self.accesstype_text

    # def userlist(self):
    #     return UserMaster.objects.filter(access_type=self.access_type, status='1')

    class Meta:
        db_table = "AccessTypeMaster"

# -------- Facility Master --------
class Facility(BaseModel):
    facility_name = models.CharField(max_length=150, blank=True,null=True)
    sr_no = models.PositiveIntegerField(unique=True)
    remarks = models.TextField(blank=True, null=True)

    class Meta:
        db_table = "Facility"

    def __str__(self):
        return self.facility_name


# -------- Room Master --------


class Room(BaseModel):

    ROOM_TYPE_CHOICES = [
        ('Single', 'Single'),
        ('Double', 'Double'),
        ('Triple', 'Triple'),
        ('Dormitory', 'Dormitory'),
    ]

    AC_TYPE_CHOICES = [
        ('AC', 'AC'),
        ('Non-AC', 'Non-AC'),
    ]

    ROOM_STATUS_CHOICES = [
        ('Available', 'Available'),
        ('Occupied', 'Occupied'),
        ('Partially_Occupied', 'Partially Occupied'),
        ('Reserved', 'Reserved'),
        ('Maintenance', 'Maintenance'),
        ('Blocked', 'Blocked'),
    ]

    room_id = models.CharField(max_length=50, unique=True, null=True, blank=True)
    room_type = models.CharField(max_length=20, choices=ROOM_TYPE_CHOICES)
    ac_non_ac = models.CharField(max_length=20, choices=AC_TYPE_CHOICES)
    room_rent = models.PositiveIntegerField(validators=[MinValueValidator(0)])

    status = models.CharField(
        max_length=20,
        choices=ROOM_STATUS_CHOICES,
        default='Available'
    )

    facility = models.ForeignKey(Facility, on_delete=models.SET_NULL, null=True)
    remarks = models.TextField(blank=True, null=True)
    extra = models.JSONField(blank=True, null=True)

    def capacity(self):
        return {
            'Single': 1,
            'Double': 2,
            'Triple': 3,
            'Dormitory': 10,
        }.get(self.room_type, 1)
    capacity.short_description = "Capacity"

    def occupied_count(self):
        if not self.pk:
            return 0
        return self.tenants.count()
    occupied_count.short_description = "Occupied"

    def is_full(self):
        return self.occupied_count() >= self.capacity()
    is_full.boolean = True
    is_full.short_description = "Is Full"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def __str__(self):
        return self.room_id or f"Room-{self.id}"

# -------- Tenant Master --------
class Tenant(BaseModel):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(unique=True)
    phone_no = models.CharField(max_length=15, unique=True)

    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)
    aadhar_no = models.CharField(max_length=12, unique=True)

    token = models.CharField(max_length=100, blank=True, null=True)
    remarks = models.TextField(blank=True, null=True)
    extra = models.JSONField(blank=True, null=True)

    address_doc = models.FileField(upload_to='tenant_docs/address/', blank=True, null=True)
    id_proof = models.FileField(upload_to='tenant_docs/id_proof/', blank=True, null=True)

    join_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)

    room = models.ForeignKey(
        Room,
        on_delete=models.SET_NULL,
        null=True,
        related_name="tenants"
    )

    pending_rent = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def clean(self):
        if self.room:
            current = Tenant.objects.filter(room=self.room).exclude(pk=self.pk).count()
            if current >= self.room.capacity():
                raise ValidationError("This room is already fully occupied.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.first_name} ({self.room})"




# -------- Electricity Bill --------
class ElectricityBill(BaseModel):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='bills')
    date_month = models.DateField()

    previous_reading = models.PositiveIntegerField()
    current_reading = models.PositiveIntegerField()
    unit_charge = models.DecimalField(max_digits=6, decimal_places=2)

    remarks = models.TextField(blank=True, null=True)
    extra = models.JSONField(blank=True, null=True)

    

    def __str__(self):
        return str(self.id)

class Tenant_history(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    changed_field = models.CharField(max_length=100)
    old_value = models.TextField()
    new_value = models.TextField()
    changed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Change in {self.tenant.first_name} - {self.changed_field} at {self.changed_at}"