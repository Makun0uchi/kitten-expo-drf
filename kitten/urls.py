from django.urls import path, include
from rest_framework import routers
from .views import (
    BreedAPIView,
    KittenViewSet,
    KittenRatingViewSet,
)


router = routers.DefaultRouter()
router.register(r'kittens', KittenViewSet)
router.register(r'ratings', KittenRatingViewSet)

urlpatterns = [
    path('breeds/', BreedAPIView.as_view(), name='breeds'),
    path('', include(router.urls)),
]
