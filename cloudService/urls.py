from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from user.views import UserViewSets, UserLoginViewSets
from explore.views import ExploreViewSet
from campaign.views import CampaignViewSet
from pvp.views import PvpViewSet
from repair.views import RepairViewSet
from build_ship.views import BuildShipViewSet
from build_equipment.views import BuildEquipmentViewSet


router = DefaultRouter()

router.register('user', UserViewSets, basename='user')
router.register('user', UserLoginViewSets, basename='user')
router.register('explore', ExploreViewSet, basename='explore')
router.register('campaign', CampaignViewSet, basename='campaign')
router.register('pvp', PvpViewSet, basename='pvp')
router.register('repair', RepairViewSet, basename='repair')
router.register('build', BuildShipViewSet, basename='build')
router.register('development', BuildEquipmentViewSet, basename='development')

urlpatterns = [
    path("", include(router.urls)),
    path('admin/', admin.site.urls),
]
