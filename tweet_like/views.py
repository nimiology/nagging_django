from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from tweet_like.models import TweetLike
from tweet_like.serializers import TweetLikeSerializer
from users.permissions import IsOwner


class TweetLikeViewSet(ModelViewSet):
    queryset = TweetLike.objects.all()
    serializer_class = TweetLikeSerializer
    filterset_fields = {'owner': ['exact'],
                        'tweet': ['exact'],
                        'created_at': ['gte', 'lte', 'exact'],
                        }
    ordering_fields = ['id',
                       'owner',
                       'tweet',
                       'created_at',
                       '?']

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [IsAuthenticated]
        elif self.action in ['destroy']:
            permission_classes = [IsOwner]
        else:
            permission_classes = []
        return [permission() for permission in permission_classes]

    def update(self, request, *args, **kwargs):
        return Response(
            {"detail": "Not allowed. Use POST to create a like."},
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )

    def partial_update(self, request, *args, **kwargs):
        return Response(
            {"detail": "Not allowed. Use POST to create a like."},
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )

    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user)
