from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from tweet.models import Tweet
from tweet.serializers import TweetSerializer
from users.permissions import IsOwner


class TweetModelViewSet(ModelViewSet):
    queryset = Tweet.objects.all()
    serializer_class = TweetSerializer
    filterset_fields = {'owner': ['exact'],
                        'reply': ['exact'],
                        'content': ['icontains'],
                        'created_at': ['gte', 'lte', 'exact'],
                        }
    ordering_fields = ['id',
                       'owner',
                       'reply',
                       'content',
                       'created_at',
                       '?']

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [IsAuthenticated]
        elif self.action in ['destroy', 'update', 'partial_update']:
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
