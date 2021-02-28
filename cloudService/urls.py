from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from user.views import UserViewSets, UserLoginViewSets

router = DefaultRouter()

router.register('user', UserViewSets, basename='user')
router.register('user', UserLoginViewSets, basename='user')

urlpatterns = [
    path("", include(router.urls)),
    path('admin/', admin.site.urls),
]
