from django.contrib.auth import authenticate
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.viewsets import ReadOnlyModelViewSet
from .models import Tenant_history
from .serializers import TenantHistorySerializer


from .models import (
    Facility, Room, Tenant, ElectricityBill,
    UserTypeMaster, LoginTypeMaster, AccessTypeMaster
)

from .serializers import (
    FacilitySerializer, RoomSerializer, TenantSerializer,
    ElectricityBillSerializer, UserTypeSerializer,
    LoginTypeSerializer, AccessTypeSerializer
)

# =========================
# LOGIN API
# =========================
class LoginAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        if not username or not password:
            return Response(
                {"error": "Username and password are required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        user = authenticate(username=username, password=password)

        if user is None:
            return Response(
                {"error": "Invalid username or password"},
                status=status.HTTP_401_UNAUTHORIZED
            )

        refresh = RefreshToken.for_user(user)

        return Response({
            "message": "Login successful",
            "access": str(refresh.access_token),
            "refresh": str(refresh)
        }, status=status.HTTP_200_OK)


# =========================
# VIEWSETS
# =========================
class FacilityViewSet(viewsets.ModelViewSet):
    queryset = Facility.objects.filter(record_status='Active')
    serializer_class = FacilitySerializer
    permission_classes = [permissions.IsAuthenticated]


class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = Room.objects.filter(record_status='Active')

        # Query parameters
        status_param = self.request.query_params.get('status')
        room_type = self.request.query_params.get('room_type')
        ac_non_ac = self.request.query_params.get('ac_non_ac')
        facility_id = self.request.query_params.get('facility')
        available = self.request.query_params.get('available')

        # Apply filters
        if status_param:
            queryset = queryset.filter(status=status_param)

        if room_type:
            queryset = queryset.filter(room_type=room_type)

        if ac_non_ac:
            queryset = queryset.filter(ac_non_ac=ac_non_ac)

        if facility_id:
            queryset = queryset.filter(facility_id=facility_id)

        # Shortcut for available rooms
        if available == 'true':
            queryset = queryset.filter(status='Available')

        return queryset
    
    # 👇 ADD THIS METHOD HERE
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if not serializer.is_valid():
            print("ROOM CREATE ERROR:", serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)



class TenantViewSet(viewsets.ModelViewSet):
    queryset = Tenant.objects.filter(record_status='Active')
    serializer_class = TenantSerializer
    permission_classes = [permissions.IsAuthenticated]


class ElectricityBillViewSet(viewsets.ModelViewSet):
    queryset = ElectricityBill.objects.filter(record_status='Active')
    serializer_class = ElectricityBillSerializer
    permission_classes = [permissions.IsAuthenticated]


class UserTypeViewSet(viewsets.ModelViewSet):
    queryset = UserTypeMaster.objects.filter(record_status='Active')
    serializer_class = UserTypeSerializer
    permission_classes = [permissions.IsAuthenticated]


class LoginTypeViewSet(viewsets.ModelViewSet):
    queryset = LoginTypeMaster.objects.filter(record_status='Active')
    serializer_class = LoginTypeSerializer
    permission_classes = [permissions.IsAuthenticated]


class AccessTypeViewSet(viewsets.ModelViewSet):
    queryset = AccessTypeMaster.objects.filter(record_status='Active')
    serializer_class = AccessTypeSerializer
    permission_classes = [permissions.IsAuthenticated]



class TenantHistoryViewSet(ReadOnlyModelViewSet):
    queryset = Tenant_history.objects.all().order_by('-changed_at')
    serializer_class = TenantHistorySerializer
