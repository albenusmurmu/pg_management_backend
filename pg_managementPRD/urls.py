"""
URL configuration for pg_managementPRD project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# ==============================
# urls.py (app level)
# ==============================
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from MASTERAPP import views
from rest_framework_simplejwt.views import TokenRefreshView
from django.http import JsonResponse

router = DefaultRouter()
router.register(r'facilities', views.FacilityViewSet)
router.register(r'rooms', views.RoomViewSet)  # or add basename='room'
router.register(r'tenants', views.TenantViewSet)
router.register(r'electricity-bills', views.ElectricityBillViewSet)
router.register(r'user-types', views.UserTypeViewSet)
router.register(r'login-types', views.LoginTypeViewSet)
router.register(r'access-types', views.AccessTypeViewSet)
router.register(r'tenant-history', views.TenantHistoryViewSet)
def health(request):
    return JsonResponse({"status": "API running"})
urlpatterns = [
    path('admin/', admin.site.urls),
    path("", health),  # 👈 ADD THIS FIRST

    # API ROUTES
    path('', include(router.urls)),

    # AUTH
    path('login/', views.LoginAPIView.as_view(), name='login'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
