from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Breed, Kitten
from .permissions import IsKittenOwner
from .serializers import BreedSerializer, KittenSerializer
from django_filters.rest_framework import DjangoFilterBackend


class BreedAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        breeds = Breed.objects.all()
        serializer = BreedSerializer(breeds, many=True)
        return Response(serializer.data)


class KittenView(viewsets.ModelViewSet):
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
