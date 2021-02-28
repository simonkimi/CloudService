from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from user.views import UserViewSets, UserLoginViewSets
from explore.views import ExploreViewSet

router = DefaultRouter()

router.register('user', UserViewSets, basename='user')
router.register('user', UserLoginViewSets, basename='user')
router.register('explore', ExploreViewSet, basename='explore')

urlpatterns = [
    path("", include(router.urls)),
    path('admin/', admin.site.urls),
]
