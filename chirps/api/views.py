from django.db.models import Q
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import ListAPIView,RetrieveAPIView,RetrieveUpdateAPIView,DestroyAPIView,CreateAPIView
from chirps.models import chirp
from .serializers import ChirpListSerializer,ChirpDetailSerializer,ChirpCreateUpdateSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly
from .permissions import IsOwnerOrReadOnly

class ChirpListAPIView(ListAPIView):
    serializer_class = ChirpListSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['content', 'user__username', 'user__first_name', 'user__last_name']

    def get_queryset(self, *args, **kwargs):
        query_set_list = chirp.objects.all()
        query = self.request.GET.get('q')
        if query:
            query_set_list = query_set_list.filter(
                    Q(content__icontains=query) |
                    Q(user__username__icontains=query) |
                    Q(user__first_name__icontains=query) |
                    Q(user__last_name__icontains=query)
            ).distinct()
        return query_set_list


class ChirpUpdateAPIView(RetrieveUpdateAPIView):
    queryset = chirp.objects.all().order_by('-timestamp')
    serializer_class = ChirpCreateUpdateSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

class ChirpDeleteAPIView(DestroyAPIView):
    queryset = chirp.objects.all()
    serializer_class = ChirpDetailSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

class ChirpDetailAPIView(RetrieveAPIView):
    queryset = chirp.objects.all()
    serializer_class = ChirpDetailSerializer

class ChirpCreateAPIView(CreateAPIView):
    queryset = chirp.objects.all()
    serializer_class = ChirpCreateUpdateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user = self.request.user)
