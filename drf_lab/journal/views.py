from django.db.models import Q
from rest_framework import filters, permissions, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response

from .models import Article, Category
from .permissions import IsAdminOrReadOnly, IsAuthorOrReadOnly
from .serializers import ArticleSerializer, CategorySerializer


# Lesson 03: the smallest possible API view.
@api_view(["GET"])
@permission_classes([permissions.AllowAny])
def hello(request):
    return Response({"message": "Hello from Django REST Framework!"})


# Lesson 06: one ViewSet = list, create, retrieve, update, partial_update and destroy.
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]


class ArticleViewSet(viewsets.ModelViewSet):
    serializer_class = ArticleSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    # Lesson 06: ?search=django  and  ?ordering=-created_at
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["title", "body"]
    ordering_fields = ["created_at", "title"]

    def get_queryset(self):
        """Everyone sees published articles. A logged-in user also sees their own drafts."""
        user = self.request.user
        queryset = Article.objects.select_related("author").prefetch_related("categories")
        if user.is_authenticated:
            queryset = queryset.filter(Q(is_published=True) | Q(author=user))
        else:
            queryset = queryset.filter(is_published=True)

        # Lesson 06: ?category=2 shows only articles in category 2
        category_id = self.request.query_params.get("category")
        if category_id:
            queryset = queryset.filter(categories__id=category_id)
        return queryset

    def perform_create(self, serializer):
        # The author is ALWAYS the logged-in user, never something the client sends.
        serializer.save(author=self.request.user)

    # Lesson 06 (bonus): an extra endpoint -> GET /api/articles/mine/
    @action(detail=False, methods=["get"], permission_classes=[permissions.IsAuthenticated])
    def mine(self, request):
        articles = self.get_queryset().filter(author=request.user)
        serializer = self.get_serializer(articles, many=True)
        return Response(serializer.data)
