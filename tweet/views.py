from rest_framework.permissions import IsAuthenticated
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

