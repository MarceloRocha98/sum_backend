"""sum_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include

from rest_framework.routers import DefaultRouter
from core.views import  UserViewSet, BlotterViewSet, listBlotters


from rest_framework_simplejwt.views import TokenVerifyView

router=DefaultRouter()
router.register(r'trading/blotter', BlotterViewSet, basename="BlotterViewSet")
router.register(r'user', UserViewSet)
router.register(r'first_task', listBlotters, basename="listBlotters")

urlpatterns = [
    path('',include(router.urls)),
    path("admin/", admin.site.urls),


    # path('api/verify/', TokenVerifyView.as_view(), name = 'TokenVerifyView'),
    # path('api/token/', TokenObtainPairView.as_view(), name = 'token_obtain_pair'),
    # path('api/token/refresh/', TokenRefreshView.as_view(), name = 'token_refresh'),
    
]