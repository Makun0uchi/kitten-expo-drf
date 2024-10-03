from django.urls import path, include
from rest_framework import routers
from .views import BreedAPIView, KittenView

router = routers.DefaultRouter()
router.register(r'kittens', KittenView)

urlpatterns = [
    path('breeds', BreedAPIView.as_view(), name='breeds'),
    path('', include(router.urls)),
]
