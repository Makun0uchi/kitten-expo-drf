from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, status
from rest_framework.mixins import (
    UpdateModelMixin,
    DestroyModelMixin,
    CreateModelMixin,
    ListModelMixin,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from .models import Breed, Kitten, KittenRating
from .permissions import IsKittenOwner, IsRatingOwner
from .serializers import (
    BreedSerializer,
    KittenSerializer,
    KittenRatingSerializer,
    KittenRatingUpdateSerializer,
)
from django_filters.rest_framework import DjangoFilterBackend


class BreedAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        breeds = Breed.objects.all()
        serializer = BreedSerializer(breeds, many=True)
        return Response(serializer.data)


class KittenViewSet(viewsets.ModelViewSet):
    queryset = Kitten.objects.all()
    serializer_class = KittenSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('breed',)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_permissions(self):
        permission_classes = {
            'list': (IsAuthenticated,),
            'retrieve': (IsAuthenticated,),
            'create': (IsAuthenticated,),
            'update': (IsAuthenticated, IsKittenOwner,),
            'partial_update': (IsAuthenticated, IsKittenOwner,),
            'destroy': (IsAuthenticated, IsKittenOwner,),
        }

        action = self.action
        return [permission() for permission in permission_classes[action]]


class KittenRatingViewSet(
    ListModelMixin,
    CreateModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
    GenericViewSet,
):
    queryset = KittenRating.objects.all()
    serializer_class = KittenRatingSerializer

    def get_serializer_class(self):
        if self.action in ['update', 'partial_update']:
            return KittenRatingUpdateSerializer
        return KittenRatingSerializer

    @swagger_auto_schema(
        operation_summary='Возвращает все оценки текущего пользователя.'
    )
    def list(self, request, *args, **kwargs):
        user = request.user
        queryset = KittenRating.objects.filter(user=user)
        serializer = KittenRatingSerializer(queryset, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_summary='Добавление оценки.'
    )
    def create(self, request, *args, **kwargs):
        user = request.user
        kitten_id = request.data['kitten']
        score = request.data['score']

        if KittenRating.objects.filter(user=user, kitten_id=kitten_id).exists():
            return Response(status=status.HTTP_400_BAD_REQUEST)
        rating = KittenRating(kitten_id=kitten_id, user=user, score=score)
        rating.save()
        serializer = KittenRatingSerializer(rating)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        try:
            rating = KittenRating.objects.get(id=self.kwargs['pk'])
        except KittenRating.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        self.check_object_permissions(request, rating)

        rating.score = request.data['score']
        rating.save()
        serializer = KittenRatingSerializer(rating)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def get_permissions(self):
        permission_classes = {
            'list': (IsAuthenticated,),
            'create': (IsAuthenticated,),
            'update': (IsAuthenticated, IsRatingOwner,),
            'partial_update': (IsAuthenticated, IsRatingOwner,),
            'destroy': (IsAuthenticated, IsRatingOwner,),
        }
        default_permissions = (IsAuthenticated,)

        action = self.action
        return [permission() for permission in permission_classes.get(action, default_permissions)]
